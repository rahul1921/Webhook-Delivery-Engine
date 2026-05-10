from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db

from schemas.pydantic_models import (
    SubscriptionRequest
)

from db.repositories.subscriber_repository import (
    SubscriberRepository
)

from services.subscription_service import (
    SubscriptionService
)

router = APIRouter()


@router.post("/")
def create_subscription(
    request: SubscriptionRequest,
    db: Session = Depends(get_db)
):

    service = SubscriptionService(
        SubscriberRepository(db)
    )

    subscriber = service.create_subscription(request)

    return subscriber


@router.get("/")
def get_all_subscriptions(
    db: Session = Depends(get_db)
):

    service = SubscriptionService(
        SubscriberRepository(db)
    )

    return service.get_all_subscriptions()


@router.get("/{subscriber_id}")
def get_subscription(
    subscriber_id: int,
    db: Session = Depends(get_db)
):

    service = SubscriptionService(
        SubscriberRepository(db)
    )

    subscriber = service.get_subscription(
        subscriber_id
    )

    if not subscriber:
        raise HTTPException(
            status_code=404,
            detail="Subscriber not found"
        )

    return subscriber


@router.put("/{subscriber_id}")
def update_subscription(
    subscriber_id: int,
    request: SubscriptionRequest,
    db: Session = Depends(get_db)
):

    service = SubscriptionService(
        SubscriberRepository(db)
    )

    subscriber = service.update_subscription(
        subscriber_id,
        request
    )

    if not subscriber:
        raise HTTPException(
            status_code=404,
            detail="Subscriber not found"
        )

    return subscriber