# Low Level Design

# Folder Structure
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

# Design Principles

- SOLID principles
- Separation of concerns
- Strategy Pattern
- Repository Pattern
- Dependency Injection

---

# API Layer

Responsible for:
- request validation
- response formatting
- dependency injection

Uses:
- FastAPI routers
- Pydantic schemas

---

# Service Layer

Contains business logic.

Examples:
- SubscriptionService
- EventService
- DeliveryService

Responsibilities:
- orchestration
- validation
- workflow management

---

# Repository Layer

Responsible for DB access.

Examples:
- SubscriberRepository
- EventRepository
- DeliveryRepository

Benefits:
- decouples ORM from business logic
- easier DB replacement

---

# Strategy Pattern

Used for:
- Signature generation

Current:
- HmacSHA256Signer

Future:
- RSA signer
- JWT signer

---

# Worker Design

Background polling loop:

while True:
    fetch pending deliveries
    process deliveries
    sleep

---

# Delivery Flow

1. Event created
2. Matching subscribers fetched
3. Delivery jobs created
4. Worker polls jobs
5. HTTP delivery attempted
6. Retry scheduled on failure

---

# Retry Logic
```
next_retry =
    now + (2 ^ attempt_count)
```
---

# Database Tables

## subscribers

- id
- url
- secret
- event_types

## events

- id
- event_type
- payload

## deliveries

- id
- event_id
- subscriber_id
- status
- attempt_count
- response_code
- last_error
- next_attempt_at

---

# Why Repository Pattern?

Without repository:
- business tightly coupled to ORM

With repository:
- easier testing
- easier migration
- cleaner code

---

# Why Dependency Injection?

Enables:
- mocking
- testing
- loose coupling

---

# Why Strategy Pattern?

Allows replacing signing algorithm
without changing worker logic.

Open/Closed Principle.

---

# Failure Handling

Handled:
- HTTP failures
- timeouts
- retries

Not handled:
- DLQ
- circuit breaker
- idempotency

---

# Future Enhancements

- Redis queue
- Kafka integration
- Horizontal scaling
- Parallel workers
- Distributed locking
- Retry queues
- Dead letter queues
