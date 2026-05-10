from db.models import Event, Delivery


class EventService:

    def __init__(
        self,
        event_repository,
        subscriber_repository,
        delivery_repository
    ):
        self.event_repository = event_repository
        self.subscriber_repository = subscriber_repository
        self.delivery_repository = delivery_repository

    def publish_event(self, request):

        event = Event(
            event_type=request.event_type,
            payload=request.payload
        )

        created_event = self.event_repository.create(event)

        subscribers = self.subscriber_repository.get_by_event_type(
            request.event_type
        )

        deliveries = []

        for subscriber in subscribers:

            deliveries.append(
                Delivery(
                    event_id=created_event.id,
                    subscriber_id=subscriber.id,
                    status="PENDING"
                )
            )

        self.delivery_repository.bulk_create(deliveries)

        return {
            "event_id": created_event.id,
            "delivery_jobs": len(deliveries)
        }

    def get_all_events(self):

        return self.event_repository.get_all()

    def get_event(self, event_id: int):

        return self.event_repository.get_by_id(event_id)