from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.session import Base

class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    event_types = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True)

    event_id = Column(Integer, ForeignKey("events.id"))
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))

    status = Column(String, default="PENDING")

    attempt_count = Column(Integer, default=0)

    response_code = Column(Integer)
    last_error = Column(String)

    next_attempt_at = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event")
    subscriber = relationship("Subscriber")
