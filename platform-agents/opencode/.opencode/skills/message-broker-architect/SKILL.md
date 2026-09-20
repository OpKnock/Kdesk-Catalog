---
name: "message-broker-architect"
description: "Selects and operates message brokers: Kafka topics, RabbitMQ queues, and NATS streams with the right delivery semantics for each workload. Use when working with kafka, rabbitmq nats or when the user mentions kafka, rabbitmq nats."
---

Selects and operates message brokers: Kafka topics, RabbitMQ queues, and NATS streams with the right delivery semantics for each workload.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-topics.sh --bootstrap-server localhost:9092 --create -`, `rabbitmqctl list_queues name messages_ready messages_unackno`
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

# Message Broker Architecture

Pick the right broker and topology for the workload.

## When to Use

- Decoupling producers and consumers
- Event sourcing and stream processing
- Work queues and fan-out

## Decision guide

- Kafka: high-throughput log/event streaming, replayable.
- RabbitMQ: flexible routing (exchanges), work queues, RPC.
- NATS: lightweight, at-most-once default, edge/microservices.

## Kafka basics

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 1
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group order-processor --describe
```

Partitions = parallelism; keep them proportional to consumers.

## RabbitMQ basics

```bash
rabbitmqctl list_queues name messages_ready messages_unacknowledged
rabbitmqadmin declare queue name=orders durable=true
```

Watch `messages_unacknowledged` - it shows stuck consumers.

## NATS JetStream

```bash
nats stream add ORDERS --subjects 'orders.>' --storage file --retention limits --max-age 168h
nats stream report ORDERS
```

## Delivery semantics

- At-most-once: fast, lossy (telemetry).
- At-least-once: redelivery + idempotent consumers.
- Exactly-once: Kafka transactions or dedupe at the store.

## Best practices

- Right-size partitions/queues for consumer concurrency.
- Monitor lag: consumer-group offsets vs latest.
- Plan for replayability in event-sourced systems.
- Never block producers on slow consumers - use dead-letter queues.

## Testing

Produce 10k messages, consume with a group, and verify zero lag and zero loss.

## Capabilities

### kafka
Administer Kafka topics and consumer groups.

**Parameters:**
- `topic` (string): Topic name
- `partitions` (number): Partition count
- `replication-factor` (number): Replication factor

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 1`
- `kafka-topics.sh --bootstrap-server localhost:9092 --list`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group order-processor --describe`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --partitions 12
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --max-messages 5
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group order-processor --reset-offsets --to-earliest --execute

### rabbitmq-nats
Manage RabbitMQ queues and NATS streams.

**Parameters:**
- `queue` (string): Queue or stream name
- `durable` (string): Survive broker restart
- `max-age` (string): Retention window like 168h

**Commands:**
- `rabbitmqctl list_queues name messages_ready messages_unacknowledged`
- `rabbitmqadmin declare queue name=orders durable=true`
- `nats stream add ORDERS --subjects 'orders.>' --storage file --retention limits --max-age 168h`
- `nats stream report ORDERS`
- `rabbitmqctl list_consumers`

**Examples:**
- rabbitmqadmin list queues name messages -f tsv
- nats stream info ORDERS | head -25
- nats consumer add ORDERS order-worker --pull --deliver last --max-deliver 5

## References
- [Kafka Docs](https://kafka.apache.org/documentation/)
- [RabbitMQ Docs](https://www.rabbitmq.com/docs)
- [NATS Docs](https://docs.nats.io/)
