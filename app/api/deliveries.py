from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.session import get_db

from services.delivery_service import DeliveryService

from db.repositories.delivery_repository import (
    DeliveryRepository
)

router = APIRouter()


@router.get("/")
def get_deliveries(
    status: Optional[str] = Query(None),
    subscriber_id: Optional[int] = Query(None),
    event_id: Optional[int] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):

    service = DeliveryService(
        DeliveryRepository(db)
    )

    return service.get_deliveries(
        status=status,
        subscriber_id=subscriber_id,
        event_id=event_id,
        limit=limit,
        offset=offset
    )