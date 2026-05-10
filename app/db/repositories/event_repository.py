from sqlalchemy.orm import Session

from db.models import Event


class EventRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, event: Event):

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event

    def get_all(self):

        return self.db.query(Event).all()

    def get_by_id(self, event_id: int):

        return self.db.query(Event).filter(
            Event.id == event_id
        ).first()