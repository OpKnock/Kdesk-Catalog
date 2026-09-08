---
name: "event-sourcing"
description: "Event-sourcing architectures: append events to event stores (Kafka, EventStoreDB), rebuild projections, and replay events for audit and recovery. Use when working with event store ops, api or when the user mentions event store ops, api."
license: "MIT"
compatibility: "Requires kafka-console-consumer, kafka-console-producer, kafka-consumer-groups. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(kafka-console-consumer:*) Bash(kafka-console-producer:*) Bash(kafka-consumer-groups:*)"
---

Event-sourcing architectures: append events to event stores (Kafka, EventStoreDB), rebuild projections, and replay events for audit and recovery.

## Agentic Workflow: Read -> Reason -> Act (event-sourcing)

You are **Event Sourcing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `event-sourcing`
- Domain: Event-sourcing architectures: append events to event stores (Kafka, EventStoreDB), rebuild projections, and replay events for audit and recovery.
- **event-store-ops**: Append and read events in EventStoreDB and Kafka, and manage projections. — `curl -s -X POST http://localhost:2113/streams/orders-1 -H 'Content-Type: applica`
- Check `knowledge` and `prerequisites: kafka-console-consumer, kafka-console-producer, kafka-consumer-groups`

### 2. Reason — think for `event-sourcing`
- For `event-store-ops`: Append and read events in EventStoreDB and Kafka, and manage projections. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `event-sourcing` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Kafka-console-producer` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `event-sourcing:e52d74a6`

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

**Parameters:**
- `topic` (string): Kafka topic or EventStoreDB stream name
- `event-type` (string): Event type like OrderPlaced
- `stream-id` (string): Aggregate stream identifier

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

## References
- [EventStoreDB HTTP API](https://developers.eventstore.com/server/v24.2/http-api/)
- [Kafka Consumers Guide](https://kafka.apache.org/documentation/)
