from db.repositories.delivery_repository import (
    DeliveryRepository
)


class DeliveryService:

    def __init__(self, repository: DeliveryRepository):
        self.repository = repository

    def get_deliveries(
        self,
        status=None,
        subscriber_id=None,
        event_id=None,
        limit=10,
        offset=0
    ):

        return self.repository.get_deliveries(
            status=status,
            subscriber_id=subscriber_id,
            event_id=event_id,
            limit=limit,
            offset=offset
        )