---
trigger: glob
description: "Engineers event-sourced services end-to-end: ksqlDB streams, consumer-group management, EventStoreDB, and Confluent tooling. Use when working with stream processing, event store and infra or when the user mentions stream processing, event store and infra."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.sql"]
---

Engineers event-sourced services end-to-end: ksqlDB streams, consumer-group management, EventStoreDB, and Confluent tooling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ksql <<< "CREATE STREAM orders (id BIGINT, total DOUBLE) WIT`, `docker compose up -d eventstore`
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

# Event Sourcing Engineering

Implement and operate event-sourced services in production.

## What This Skill Does

- Builds stream processing with ksqlDB and Kafka Streams
- Resets and replays stream applications
- Manages consumer groups and offsets
- Operates EventStoreDB infrastructure
- Provisions Confluent resources from the CLI

## When to Use

- Standing up an event-sourced service
- Reprocessing events after a deployment bug
- Production Kafka/EventStore operations

## Real Commands

```bash
# ksqlDB
ksql <<< "CREATE STREAM orders (id BIGINT, total DOUBLE)   WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='JSON');"
ksql <<< "CREATE TABLE totals AS   SELECT id, SUM(total) AS sum FROM orders GROUP BY id EMIT CHANGES;"
ksql <<< "SHOW STREAMS;"
ksql <<< "SHOW TABLES;"

# Streams reset (replay)
kafka-streams-application-reset.sh   --bootstrap-server localhost:9092   --application-id stream-app --input-topics orders
kafka-consumer-groups.sh --bootstrap-server localhost:9092   --reset-offsets --group stream-app --to-earliest --execute

# EventStoreDB
docker compose up -d eventstore
curl -s http://localhost:2113/streams/orders/metadata | jq '.maxCount'

# Confluent
confluent login
confluent environment list
confluent kafka topic create payments --partitions 6
confluent kafka topic describe payments
```

## Deployment Checklist

1. Event schema registered and versioned
2. Consumer groups have committed offsets
3. Streams app restartable via reset tool
4. Projections idempotent and replayable
5. Retention matches replay windows

## Best Practices

- Use ksqlDB for simple aggregations; Kafka Streams for complex logic
- Reset applications in staging before prod replays
- Monitor consumer lag on every topic
- Snapshot aggregates; rebuild from events when logic changes
- Test schema evolution with a compat checker in CI

## Capabilities

### stream-processing
Build stream processing with ksqlDB and Kafka Streams.

**Parameters:**
- `app-id` (string): Kafka Streams application id
- `topic` (string): Input topic

**Commands:**
- `ksql <<< "CREATE STREAM orders (id BIGINT, total DOUBLE) WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='JSON');"`
- `ksql <<< "CREATE TABLE totals AS SELECT id, SUM(total) AS sum FROM orders GROUP BY id EMIT CHANGES;"`
- `kafka-streams-application-reset.sh --bootstrap-server localhost:9092 --application-id stream-app --input-topics orders`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group stream-app --to-earliest --execute`
- `ksql <<< 'SHOW STREAMS;'`

**Examples:**
- ksql <<< "CREATE STREAM orders ..."
- kafka-streams-application-reset.sh --application-id stream-app --input-topics orders
- ksql <<< "SHOW STREAMS;"

### event-store-and-infra
Operate EventStoreDB and Confluent infrastructure.

**Parameters:**
- `topic` (string): Topic name
- `partitions` (integer): Partition count

**Commands:**
- `docker compose up -d eventstore`
- `curl -s http://localhost:2113/streams/orders/metadata | jq '.maxCount'`
- `confluent login`
- `confluent kafka topic create payments --partitions 6`
- `confluent kafka topic describe payments`
- `confluent environment list`

**Examples:**
- docker compose up -d eventstore
- confluent kafka topic create payments --partitions 6
- confluent kafka topic describe payments

## References
- [ksqlDB Documentation](https://docs.ksqldb.io/)
- [Kafka Streams](https://kafka.apache.org/documentation/streams/)
- [EventStoreDB Developer Docs](https://developers.eventstore.com/)
