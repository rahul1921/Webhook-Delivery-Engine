import asyncio

from fastapi import FastAPI

from db.session import Base, engine

from api.subscriptions import router as subscription_router
from api.events import router as event_router
from api.deliveries import router as delivery_router

from services.worker import worker

app = FastAPI(title="Webhook Delivery Engine")

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker.start())

@app.get("/")
def health_check():
    return {"status": "running"}

app.include_router(
    subscription_router,
    prefix="/subscriptions",
    tags=["subscriptions"]
)

app.include_router(
    event_router,
    prefix="/events",
    tags=["events"]
)

app.include_router(
    delivery_router,
    prefix="/deliveries",
    tags=["deliveries"]
)
