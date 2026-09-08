---
name: "event-driven-architect-event-driven-architect"
description: "Designs event-driven systems on Kafka, RabbitMQ, NATS, and Pulsar: topics, queues, consumers, offsets, and stream operations. Use when working with kafka operations, brokers and streams or when the user mentions kafka operations, brokers and streams."
license: "MIT"
compatibility: "Requires kafka, eventstore, redis, node.js, python, axon-server."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(kafka-console-consumer.sh:*) Bash(kafka-console-producer.sh:*) Bash(kafka-consumer-groups.sh:*) Bash(kafka-topics.sh:*) Bash(nats:*) Bash(pulsar-admin:*) Bash(rabbitmqctl:*)"
---

Designs event-driven systems on Kafka, RabbitMQ, NATS, and Pulsar: topics, queues, consumers, offsets, and stream operations.

## Agentic Workflow: Read -> Reason -> Act (event-driven-architect-event-driven-architect)

You are **event-driven-architect-event-driven-architect** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `event-driven-architect-event-driven-architect`
- Domain: Designs event-driven systems on Kafka, RabbitMQ, NATS, and Pulsar: topics, queues, consumers, offsets, and stream operations.
- **kafka-operations**: Create topics, produce/consume events, and manage consumer groups. — `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --part`
- **brokers-and-streams**: Operate RabbitMQ, NATS, and Pulsar brokers. — `rabbitmqctl status`
- Check `knowledge` and `prerequisites: kafka, eventstore, redis, node.js`

### 2. Reason — think for `event-driven-architect-event-driven-architect`
- For `kafka-operations`: Create topics, produce/consume events, and manage consumer groups. — decide which checks to run
- For `brokers-and-streams`: Operate RabbitMQ, NATS, and Pulsar brokers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `event-driven-architect-event-driven-architect` tools
- Tools: `Glob`, `Grep`, `Read`, `Kafka-topics.sh`, `Kafka-console-producer.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `event-driven-architect-event-driven-architect:f7393a51`

# Event-Driven Architecture

Design and operate event streaming and messaging systems.

## What This Skill Does

- Creates topics and manages partitions/replication
- Produces and consumes events from the CLI
- Inspects consumer group lag and offsets
- Operates RabbitMQ/NATS/Pulsar brokers
- Advises on event contracts and schemas

## When to Use

- Designing a new event flow between services
- Debugging consumer lag or missed events
- Choosing between broker technologies

## Real Commands

```bash
# Kafka
kafka-topics.sh --bootstrap-server localhost:9092 --create   --topic orders --partitions 6 --replication-factor 3
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments

# RabbitMQ
rabbitmqctl status
rabbitmqctl list_queues name messages consumers
rabbitmqctl list_bindings

# NATS
nats pub orders.new '{"id":1}'
nats sub orders.>
nats stream add ORDERS --subjects 'orders.>' --storage file

# Pulsar
pulsar-admin topics list public/default
pulsar-admin topics stats persistent://public/default/orders
```

## Design Rules

- Partition by key for ordering per entity
- Design events as facts: immutable, versioned
- Handle out-of-order and duplicate delivery (idempotency)
- Keep brokers outside the request path
- Schema-register event payloads for compatibility

## Best Practices

- Monitor consumer lag as a core SLO
- Use dead-letter topics for poison messages
- Back-pressure consumers, never unbounded buffers
- Test broker failover with partition leadership moves
- Version topics (orders.v1) for breaking changes

## Capabilities

### kafka-operations
Create topics, produce/consume events, and manage consumer groups.

**Parameters:**
- `topic` (string): Topic name
- `bootstrap-server` (string): Kafka broker address
- `partitions` (integer): Partition count

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 3`
- `kafka-topics.sh --bootstrap-server localhost:9092 --list`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments

### brokers-and-streams
Operate RabbitMQ, NATS, and Pulsar brokers.

**Parameters:**
- `subject` (string): NATS subject
- `queue` (string): RabbitMQ queue name

**Commands:**
- `rabbitmqctl status`
- `rabbitmqctl list_queues name messages consumers`
- `rabbitmqctl list_bindings`
- `nats pub orders.new '{"id":1}'`
- `nats sub orders.>`
- `pulsar-admin topics list public/default`

**Examples:**
- rabbitmqctl list_queues name messages consumers
- nats pub orders.new '{"id":1}'
- pulsar-admin topics list public/default

## References
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/docs)
- [NATS Documentation](https://docs.nats.io/)
- [Apache Pulsar](https://pulsar.apache.org/docs/)
