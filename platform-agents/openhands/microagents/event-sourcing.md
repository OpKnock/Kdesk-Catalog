---
name: "event-sourcing"
description: "Event-sourcing architectures: append events to event stores (Kafka, EventStoreDB), rebuild projections, and replay events for audit and recovery."
type: knowledge
triggers: ["event-sourcing", "event-store-ops"]
---

# Event Sourcing

Event-sourcing architectures: append events to event stores (Kafka, EventStoreDB), rebuild projections, and replay events for audit and recovery.

## Instructions

# Event Sourcing

## What this skill does

Event sourcing stores state changes as immutable events rather than the current state. Aggregates are rebuilt by replaying events; projections produce read models. This skill covers event stores and replays.

## When to use

- Designing audit-complete systems (finance, compliance)
- Rebuilding a read model from scratch
- Debugging why a projection lagged

## Real commands

```bash
# Append an event to EventStoreDB
curl -s -X POST http://localhost:2113/streams/orders-1 -H 'Content-Type: application/vnd.eventstore.events+json' -d @order-event.json

# Read a stream forward
curl -s http://localhost:2113/streams/orders-1/0/forward/20 | jq '.entries[].eventType'

# Produce and consume on Kafka
kafka-console-producer --bootstrap-server localhost:9092 --topic orders.events
kafka-console-consumer --bootstrap-server localhost:9092 --topic orders.events --from-beginning

# Projection lag
kafka-consumer-groups --bootstrap-server localhost:9092 --group projections --describe
```

## Event JSON example

```json
{
  "eventId": "3f3c3b24-1f4b-4b2c-9c1a-0c0d0e0f1a2b",
  "eventType": "OrderPlaced",
  "data": {"orderId": "o-1", "amount": 4200}
}
```

## Rebuild workflow

```bash
# 1. Stop the projection consumer
kafka-consumer-groups --bootstrap-server localhost:9092 --group projections --reset-offsets --to-earliest --execute
# 2. Let it replay from the first event
# 3. Verify counts match the original aggregate totals
```

## Best practices

- Never mutate or delete events; write corrections as new events.
- Version your event schemas (v1, v2) and keep old readers working.
- Idempotent projections: replay must yield the same read model.
- Use a dedicated topic per aggregate type to keep replay simple.
- Store event type names as constants shared across services.

## Capabilities

### event-store-ops
Append and read events in EventStoreDB and Kafka, and manage projections.

**Commands:**
- `curl -s -X POST http://localhost:2113/streams/orders-1 -H 'Content-Type: application/vnd.eventstore.events+json' -d '["{\"eventId\":\"$(uuidgen)\",\"eventType\":\"OrderPlaced\",\"data\":{\"amount\":42}}"]'`
- `curl -s http://localhost:2113/streams/orders-1/0/forward/20 | jq '.entries[].eventType'`
- `kafka-console-producer --bootstrap-server localhost:9092 --topic orders.events`
- `kafka-console-consumer --bootstrap-server localhost:9092 --topic orders.events --from-beginning`
- `kafka-consumer-groups --bootstrap-server localhost:9092 --group projections --describe`

**Examples:**
- kafka-console-producer --bootstrap-server localhost:9092 --topic orders.events
- curl -s http://localhost:2113/streams/orders-1/0/forward/20 | jq '.entries[].eventType'
- kafka-consumer-groups --bootstrap-server localhost:9092 --group projections --describe
