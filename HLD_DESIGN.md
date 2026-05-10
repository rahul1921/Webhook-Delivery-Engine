# High Level Design

# Goal

Build a scalable asynchronous webhook delivery engine.

---

# Requirements

## Functional

- Register webhooks
- Publish events
- Async delivery
- HMAC signing
- Retry failed deliveries
- Delivery logs

## Non Functional

- Reliability
- Scalability
- Fault tolerance
- Observability
- Extensibility

---

# High Level Components

1. API Layer
2. Service Layer
3. Persistence Layer
4. Background Worker
5. External Subscribers

---

# Architecture Flow

Client
  |
  v
FastAPI APIs
  |
  v
SQLite DB
  |
  v
Background Worker
  |
  v
Webhook Subscribers

---

# Core APIs

## Subscription APIs

POST /subscriptions/
GET /subscriptions/
PUT /subscriptions/{id}

## Event APIs

POST /events/
GET /events/

## Delivery APIs

GET /deliveries/

---

# Delivery Lifecycle

PENDING
   |
   v
PROCESSING
   |
   +----> SUCCESS
   |
   +----> RETRY
               |
               v
            FAILED

---

# Retry Mechanism

Exponential Backoff:

2^attempt seconds

Max attempts: 5

---

# Why Async Delivery?

Webhook delivery is network-bound.

Async processing:
- increases throughput
- reduces API latency
- prevents blocking

---

# Scalability Improvements

Current:
- SQLite
- Single worker

Production:
- PostgreSQL
- Kafka/RabbitMQ
- Distributed workers
- Kubernetes autoscaling

---

# Security

Payload signing:
- HMAC-SHA256
- Shared secret validation

---

# Observability

Current:
- Delivery logs
- DB tracking

Future:
- Prometheus
- Grafana
- OpenTelemetry

---

# Tradeoffs

Why SQLite?
- Simple
- Lightweight
- Easy assignment setup

Why polling worker?
- Simpler than queue infra
- Easier demonstration

Why service/repository pattern?
- Separation of concerns
- Maintainability
- Testability