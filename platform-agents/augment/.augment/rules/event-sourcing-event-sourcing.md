---
type: agent_requested
description: "Implements event sourcing with EventStoreDB, Kafka, projections, and CQRS read models using real CLI tooling."
---

# event-sourcing-event-sourcing

Implements event sourcing with EventStoreDB, Kafka, projections, and CQRS read models using real CLI tooling.

## Instructions

# Event Sourcing Implementation

Build systems where the event log is the source of truth.

## What This Skill Does

- Runs EventStoreDB and writes/reads streams
- Implements projections and read models (CQRS)
- Produces/replays events on Kafka
- Rebuilds read models from scratch
- Advises on event schema and versioning

## When to Use

- An audit-required domain (finance, compliance)
- Complex state transitions needing full history
- Rebuilding projections after schema changes

## Real Commands

```bash
# EventStoreDB
docker run -d -p 2113:2113 -p 1113:1113 eventstore/eventstore:latest --insecure
curl -s http://localhost:2113/streams/orders -H 'Accept: application/json' | jq '.entries[0].title'
curl -s -X POST http://localhost:2113/streams/orders   -H 'Content-Type: application/vnd.eventstore.events+json'   -d '[{"eventId":"...","eventType":"OrderCreated","data":{"id":"1","total":99}}]'
curl -s http://localhost:2113/projections/any -H 'Accept: application/json' | jq '.projections[].name'

# Kafka pipeline
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic account.events --partitions 4
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic account.events
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic account.events --from-beginning

# Rebuild projections
kafka-consumer-groups.sh --bootstrap-server localhost:9092   --reset-offsets --group projection --to-earliest --topic account.events --execute
redis-cli GET account:42:balance
```

## Core Rules

- Events are immutable facts, never edited or deleted
- Rebuild any read model by replaying the log
- Commands validate, events record outcomes
- Version events; consumers tolerate old versions
- Projections are disposable: store only the log permanently

## Best Practices

- Write the event schema before the code
- Test replay determinism in CI
- Idempotent projections for safe rebuilds
- Snapshot long streams for performance
- Use CDC (Debezium) to migrate legacy tables into events

## Capabilities

### event-store-operations
Run and interact with EventStoreDB streams.

**Commands:**
- `docker run -d -p 2113:2113 -p 1113:1113 eventstore/eventstore:latest --insecure`
- `curl -s http://localhost:2113/streams/orders | jq '.entries[0].title'`
- `curl -s -X POST http://localhost:2113/streams/orders -H 'Content-Type: application/vnd.eventstore.events+json'`
- `curl -s http://localhost:2113/streams/orders/0 -H 'Accept: application/json' | jq '.data'`
- `curl -s http://localhost:2113/projections/any -H 'Accept: application/json' | jq '.projections[].name'`

**Examples:**
- docker run -d -p 2113:2113 eventstore/eventstore:latest --insecure
- curl -s http://localhost:2113/streams/orders | jq '.entries[0].title'
- curl -s http://localhost:2113/streams/orders/0 | jq '.data'

### kafka-event-pipeline
Produce, consume, and replay events through Kafka.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic account.events --partitions 4`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic account.events`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic account.events --from-beginning`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group projection --to-earliest --topic account.events --execute`
- `redis-cli GET account:42:balance`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic account.events --partitions 4
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group projection --to-earliest --execute
- redis-cli GET account:42:balance