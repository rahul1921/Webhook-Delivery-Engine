from db.models import Subscriber
from db.repositories.subscriber_repository import (
    SubscriberRepository
)


class SubscriptionService:

    def __init__(self, repository: SubscriberRepository):
        self.repository = repository

    def create_subscription(self, request):

        subscriber = Subscriber(
            url=str(request.url),
            secret=request.secret,
            event_types=request.event_types
        )

        return self.repository.create(subscriber)

    def get_all_subscriptions(self):

        return self.repository.get_all()

    def get_subscription(self, subscriber_id: int):

        return self.repository.get_by_id(subscriber_id)

    def update_subscription(
        self,
        subscriber_id,
        request
    ):

        subscriber = self.repository.get_by_id(
            subscriber_id
        )

        if not subscriber:
            return None

        subscriber.url = str(request.url)
        subscriber.secret = request.secret
        subscriber.event_types = request.event_types

        return self.repository.update(subscriber)