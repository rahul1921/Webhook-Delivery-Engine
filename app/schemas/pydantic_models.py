from typing import List, Dict, Any
from pydantic import BaseModel, HttpUrl

class SubscriptionRequest(BaseModel):
    url: HttpUrl
    secret: str
    event_types: List[str]

class EventRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]
