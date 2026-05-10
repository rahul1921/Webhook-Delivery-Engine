import asyncio
from datetime import datetime

from db.session import SessionLocal
from db.repositories.delivery_repository import DeliveryRepository

from services.dispatcher import WebhookDispatcher

from strategies.hmac_sha256_signer import HmacSHA256Signer
from strategies.exponential_backoff_strategy import (
    ExponentialBackoffStrategy
)

MAX_RETRIES = 5

class DeliveryWorker:

    def __init__(
        self,
        dispatcher,
        signer,
        retry_strategy
    ):
        self.dispatcher = dispatcher
        self.signer = signer
        self.retry_strategy = retry_strategy

    async def process_delivery(self, delivery, repository):

        payload = delivery.event.payload
        subscriber = delivery.subscriber

        signature = self.signer.sign(
            subscriber.secret,
            payload
        )

        try:
            response = await self.dispatcher.dispatch(
                subscriber.url,
                payload,
                signature
            )

            delivery.response_code = response.status_code

            if 200 <= response.status_code < 300:
                delivery.status = "SUCCESS"
            else:
                raise Exception(f"HTTP {response.status_code}")

        except Exception as e:

            delivery.attempt_count += 1
            delivery.last_error = str(e)

            if delivery.attempt_count >= MAX_RETRIES:
                delivery.status = "FAILED"
            else:
                delivery.status = "RETRY"
                delivery.next_attempt_at = (
                    self.retry_strategy.next_retry(
                        delivery.attempt_count
                    )
                )

        delivery.updated_at = datetime.utcnow()

        repository.save()

    async def start(self):

        while True:
            db = SessionLocal()

            try:
                repository = DeliveryRepository(db)

                jobs = repository.get_pending_jobs()

                tasks = []

                for job in jobs:
                    tasks.append(
                        self.process_delivery(job, repository)
                    )

                if tasks:
                    await asyncio.gather(*tasks)

            except Exception as e:
                print("Worker Error", e)

            finally:
                db.close()

            await asyncio.sleep(2)

worker = DeliveryWorker(
    dispatcher=WebhookDispatcher(),
    signer=HmacSHA256Signer(),
    retry_strategy=ExponentialBackoffStrategy()
)
