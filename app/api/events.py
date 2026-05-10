from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db

from schemas.pydantic_models import (
    EventRequest
)

from db.repositories.event_repository import (
    EventRepository
)

from db.repositories.subscriber_repository import (
    SubscriberRepository
)

from db.repositories.delivery_repository import (
    DeliveryRepository
)

from services.event_service import EventService

router = APIRouter()


@router.post("/")
def publish_event(
    request: EventRequest,
    db: Session = Depends(get_db)
):

    service = EventService(
        event_repository=EventRepository(db),
        subscriber_repository=SubscriberRepository(db),
        delivery_repository=DeliveryRepository(db)
    )

    return service.publish_event(request)


@router.get("/")
def get_all_events(
    db: Session = Depends(get_db)
):

    service = EventService(
        event_repository=EventRepository(db),
        subscriber_repository=SubscriberRepository(db),
        delivery_repository=DeliveryRepository(db)
    )

    return service.get_all_events()


@router.get("/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    service = EventService(
        event_repository=EventRepository(db),
        subscriber_repository=SubscriberRepository(db),
        delivery_repository=DeliveryRepository(db)
    )

    event = service.get_event(event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event