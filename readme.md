# Webhook Delivery Engine

A production-style asynchronous webhook delivery platform built using:

- FastAPI
- SQLAlchemy
- SQLite
- asyncio background workers
- httpx.AsyncClient
- Pydantic

---

# Features

- Webhook subscription management
- Event publishing
- Async webhook fanout
- HMAC-SHA256 payload signing
- Exponential retry with backoff
- Delivery tracking
- Delivery log APIs
- Fault-tolerant worker model
- SQLite persistence

---

# Architecture
```
Producer Services
        |
        v
+-------------------+
| Webhook Engine    |
|-------------------|
| Event APIs        |
| Subscription APIs |
| Delivery Worker   |
+-------------------+
        |
        v
Subscriber Webhooks
```
---

# Project Structure
```
app/
├── api/
├── services/
├── strategies/
├── db/
├── schemas/
├── worker/
└── main.py
```
---

# Setup

## Create Virtual Environment


python3 -m venv venv
source venv/bin/activate



## Install Dependencies
```
pip install -r requirements.txt
```

## Start Main Service
```
cd app
uvicorn main:app --reload
```

## Start Mock Receiver
```
uvicorn mock_receiver:app --port 9000 --reload
```

## Swagger
### Main API:
```
http://127.0.0.1:8000/docs
```

### Mock Receiver:
```
http://127.0.0.1:9000/docs
```


## Register Subscription
```
curl -X POST http://127.0.0.1:8000/subscriptions/ \
-H "Content-Type: application/json" \
-d '{
  "url": "http://127.0.0.1:9000/webhook",
  "secret": "mysecret",
  "event_types": ["order.created"]
}'
```

## Publish Event
```
curl -X POST http://127.0.0.1:8000/events/ \
-H "Content-Type: application/json" \
-d '{
  "event_type": "order.created",
  "payload": {
    "order_id": 101
  }
}'
```

## Delivery Logs
```
curl http://127.0.0.1:8000/deliveries/
```

## Retry Strategy
```
Retries use exponential backoff:

Attempt 1 → 2 sec
Attempt 2 → 4 sec
Attempt 3 → 8 sec
Attempt 4 → 16 sec
Attempt 5 → FAILED
```
## Security

### Payloads are signed using: HMAC-SHA256

### Header: X-Signature


