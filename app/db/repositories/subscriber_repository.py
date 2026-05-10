from sqlalchemy.orm import Session

from db.models import Subscriber


class SubscriberRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, subscriber: Subscriber):
        self.db.add(subscriber)
        self.db.commit()
        self.db.refresh(subscriber)

        return subscriber

    def get_all(self):
        return self.db.query(Subscriber).all()

    def get_by_id(self, subscriber_id: int):

        return self.db.query(Subscriber).filter(
            Subscriber.id == subscriber_id
        ).first()

    def update(self, subscriber):

        self.db.commit()
        self.db.refresh(subscriber)

        return subscriber

    def get_by_event_type(self, event_type: str):

        subscribers = self.db.query(Subscriber).all()

        return [
            s for s in subscribers
            if event_type in s.event_types
        ]