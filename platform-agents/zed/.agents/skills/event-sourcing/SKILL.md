---
name: "event-sourcing"
description: "Event-sourcing architectures: append events to event stores (Kafka, EventStoreDB), rebuild projections, and replay events for audit and recovery. Use when working with event store ops, api or when the user mentions event store ops, api."
license: "MIT"
compatibility: "Requires kafka-console-consumer, kafka-console-producer, kafka-consumer-groups. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(kafka-console-consumer:*) Bash(kafka-console-producer:*) Bash(kafka-consumer-groups:*)"
---

Event-sourcing architectures: append events to event stores (Kafka, EventStoreDB), rebuild projections, and replay events for audit and recovery.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -X POST http://localhost:2113/streams/orders-1 -H 'C`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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
