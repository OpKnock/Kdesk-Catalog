---
name: "message-queue"
description: "Operates message brokers (RabbitMQ, Redis, NATS) for reliable pub/sub, work queues, and routing with durability and DLX handling. Use when working with rabbitmq ops, broker utilization, backend or when the user mentions rabbitmq ops, broker utilization, backend."
license: "MIT"
compatibility: "Requires nats, rabbitmqadmin, rabbitmqctl, redis-cli."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(nats:*) Bash(rabbitmqadmin:*) Bash(rabbitmqctl:*) Bash(redis-cli:*)"
---

Operates message brokers (RabbitMQ, Redis, NATS) for reliable pub/sub, work queues, and routing with durability and DLX handling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rabbitmqctl list_queues name messages_ready messages_unackno`, `redis-cli llen work:queue`
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

# Message Queue

Operate brokers for reliable asynchronous messaging.

## When to Use

- Decoupling producers from consumers
- Buffering bursts that consumers cannot keep up with
- Fan-out to multiple subscribers
- Work distribution with acknowledgments and redelivery

## Core Concepts

- Queue: durable buffer of messages
- Exchange: routing rules (direct, topic, fanout)
- Binding: queue-to-exchange route
- Ack: consumer confirmation; redelivery without it
- Dead-letter exchange: poison message parking

## Commands

```bash
# RabbitMQ inspection
rabbitmqctl list_queues name messages_ready messages_unacknowledged
rabbitmqctl list_exchanges name type
rabbitmqctl status
rabbitmq-diagnostics ping

# Declare resources
rabbitmqadmin declare queue name=emails durable=true
rabbitmqadmin declare exchange name=orders type=topic

# NATS
nats pub orders.created '{"id":1}'
nats sub "orders.*" --raw
nats stream ls

# Redis
redis-cli llen work:queue
redis-cli pubsub numsub orders
```

## Best Practices

- Make queues durable and messages persistent for critical paths
- Ack only after successful processing to avoid loss
- Route failures to a dead-letter exchange instead of dropping
- Use prefetch limits so one consumer is not swamped
- Monitor queue depth and unacked counts continuously
- Design consumers to be idempotent; redelivery happens

## Capabilities

### rabbitmq-ops
Manage RabbitMQ exchanges, queues, and bindings.

**Parameters:**
- `queue` (string): Queue name
- `exchange` (string): Exchange name
- `routing-key` (string): Binding routing key

**Commands:**
- `rabbitmqctl list_queues name messages_ready messages_unacknowledged`
- `rabbitmqadmin declare queue name=emails durable=true`
- `rabbitmqadmin declare exchange name=orders type=topic`
- `rabbitmqctl list_exchanges name type`
- `rabbitmqctl status`

**Examples:**
- rabbitmqadmin declare binding source=orders destination=email-svc routing_key=order.created
- rabbitmqctl list_queues | awk "{print $1}"
- rabbitmq-diagnostics ping

### broker-utilization
Monitor broker health and consumer state.

**Parameters:**
- `subject` (string): NATS subject
- `pattern` (string): Key pattern

**Commands:**
- `redis-cli llen work:queue`
- `redis-cli pubsub channels`
- `nats sub "orders.*" --raw`
- `nats pub orders.created "{\"id\":1}"`
- `rabbitmqctl list_consumers`

**Examples:**
- nats stream ls
- redis-cli pubsub numsub orders
- rabbitmqctl list_channels | head -20

## References
- [RabbitMQ Docs](https://www.rabbitmq.com/documentation.html)
- [NATS Docs](https://docs.nats.io)
- [Redis Pub/Sub](https://redis.io/docs/latest/develop/data-types/pubsub/)
