---
name: "event-sourcing-event-sourcing"
description: "Implements event sourcing with EventStoreDB, Kafka, projections, and CQRS read models using real CLI tooling. Use when working with event store operations, kafka event pipeline or when the user mentions event store operations, kafka event pipeline."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Implements event sourcing with EventStoreDB, Kafka, projections, and CQRS read models using real CLI tooling.

## Agentic Workflow: Read -> Reason -> Act (event-sourcing-event-sourcing)

You are **event-sourcing-event-sourcing** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `event-sourcing-event-sourcing`
- Domain: Implements event sourcing with EventStoreDB, Kafka, projections, and CQRS read models using real CLI tooling.
- **event-store-operations**: Run and interact with EventStoreDB streams. — `docker run -d -p 2113:2113 -p 1113:1113 eventstore/eventstore:latest --insecure`
- **kafka-event-pipeline**: Produce, consume, and replay events through Kafka. — `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic account.event`
- Check `knowledge` and `prerequisites: node.js, typescript, postgresql, redis`

### 2. Reason — think for `event-sourcing-event-sourcing`
- For `event-store-operations`: Run and interact with EventStoreDB streams. — decide which checks to run
- For `kafka-event-pipeline`: Produce, consume, and replay events through Kafka. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `event-sourcing-event-sourcing` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Kafka-topics.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `event-sourcing-event-sourcing:6b9d1cdd`

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

**Parameters:**
- `stream` (string): Stream name
- `event` (string): Event type

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

**Parameters:**
- `topic` (string): Event topic name
- `group` (string): Consumer group for replay

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

## References
- [EventStoreDB Documentation](https://developers.eventstore.com/)
- [Debezium](https://debezium.io/documentation/)
- [CQRS by Fowler](https://martinfowler.com/bliki/CQRS.html)