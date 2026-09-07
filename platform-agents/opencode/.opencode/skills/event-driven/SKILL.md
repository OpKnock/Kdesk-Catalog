---
name: "event-driven"
description: "Architects event-driven systems with Kafka/Redpanda: topics, producers, consumers, consumer groups, and dead-letter handling. Use when working with kafka topics, kafka streams, backend or when the user mentions kafka topics, kafka streams, backend."
---

Architects event-driven systems with Kafka/Redpanda: topics, producers, consumers, consumer groups, and dead-letter handling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-topics --bootstrap-server localhost:9092 --create --to`, `kafka-console-producer --bootstrap-server localhost:9092 --t`
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

# Event-Driven Architecture

Design systems that communicate through events.

## When to Use

- Decoupling services so producers and consumers evolve independently
- Capturing facts (order placed, user signed up) as immutable events
- Fanning out to many consumers from one source of truth
- Replaying history for analytics or recovery

## Core Concepts

- Topic: named channel of events, partitioned for parallelism
- Partition: ordered, append-only log of messages
- Consumer group: cooperating consumers that split partitions
- Offset: position of a consumer within a partition
- Dead-letter topic: destination for undeliverable events

## Commands

```bash
# Create a topic
kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 1

# List and describe
kafka-topics --bootstrap-server localhost:9092 --list
kafka-topics --describe --topic orders

# Produce
kafka-console-producer --bootstrap-server localhost:9092 --topic orders

# Consume from beginning
kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning

# Consumer group inspection
kafka-consumer-groups --bootstrap-server localhost:9092 --group order-svc --describe

# Reset offsets
kafka-consumer-groups --group order-svc --reset-offsets --to-earliest --execute
```

## Best Practices

- Partition by the entity key so per-entity ordering is preserved
- Make consumers idempotent; at-least-once delivery means replays
- Size partitions for the peak write rate, not today's load
- Forward poison messages to a dead-letter topic with headers
- Define schema (Avro/JSON Schema) and enforce compatibility
- Never couple consumers to producer implementation details

## Capabilities

### kafka-topics
Create, list, and describe Kafka topics.

**Parameters:**
- `topic` (string): Topic name
- `partitions` (integer): Partition count

**Commands:**
- `kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 1`
- `kafka-topics --bootstrap-server localhost:9092 --list`
- `kafka-topics --describe --topic orders`
- `kafka-topics --alter --topic orders --partitions 12`
- `kafka-topics --delete --topic legacy_orders`

**Examples:**
- kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 6
- kafka-topics --describe --topic orders --under-replicated-partitions
- kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --alter --add-config retention.ms=604800000

### kafka-streams
Produce and consume messages, inspect consumer groups.

**Parameters:**
- `group` (string): Consumer group id
- `from-beginning` (boolean): Read all messages from the start

**Commands:**
- `kafka-console-producer --bootstrap-server localhost:9092 --topic orders`
- `kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning`
- `kafka-consumer-groups --bootstrap-server localhost:9092 --group order-svc --describe`
- `kafka-consumer-groups --list --bootstrap-server localhost:9092`
- `kafka-get-offsets --bootstrap-server localhost:9092 --topic orders`

**Examples:**
- kafka-console-consumer --topic orders --group debug-consumer --from-beginning
- kafka-consumer-groups --group order-svc --reset-offsets --to-earliest --execute
- kafka-console-producer --topic orders --property parse.key=true --property key.separator=:

## References
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Redpanda Docs](https://docs.redpanda.com)
