from sqlalchemy.orm import Session
from datetime import datetime

from db.models import Delivery


class DeliveryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, delivery: Delivery):

        self.db.add(delivery)
        self.db.commit()
        self.db.refresh(delivery)

        return delivery

    def bulk_create(self, deliveries):

        self.db.add_all(deliveries)
        self.db.commit()

    def get_pending_jobs(
        self,
        limit: int = 10
    ):

        return self.db.query(Delivery).filter(
            Delivery.status.in_(["PENDING", "RETRY"]),
            Delivery.next_attempt_at <= datetime.utcnow()
        ).limit(limit).all()

    def get_deliveries(
        self,
        status=None,
        subscriber_id=None,
        event_id=None,
        limit=10,
        offset=0
    ):

        query = self.db.query(Delivery)

        if status:
            query = query.filter(
                Delivery.status == status
            )

        if subscriber_id:
            query = query.filter(
                Delivery.subscriber_id == subscriber_id
            )

        if event_id:
            query = query.filter(
                Delivery.event_id == event_id
            )

        return query.offset(offset).limit(limit).all()

    def save(self):
        self.db.commit()