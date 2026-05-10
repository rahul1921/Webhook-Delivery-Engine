import httpx

from interfaces.dispatcher_interface import (
    DispatcherInterface
)

class WebhookDispatcher(DispatcherInterface):

    async def dispatch(
        self,
        url,
        payload,
        signature
    ):

        async with httpx.AsyncClient(timeout=5) as client:

            response = await client.post(
                url,
                json=payload,
                headers={
                    "X-Signature": signature,
                    "Content-Type": "application/json"
                }
            )

        return response
