---
type: agent_requested
description: "Operates message brokers (RabbitMQ, Redis, NATS) for reliable pub/sub, work queues, and routing with durability and DLX handling. Use when working with rabbitmq ops, broker utilization, backend or when the user mentions rabbitmq ops, broker utilization, backend."
---

Operates message brokers (RabbitMQ, Redis, NATS) for reliable pub/sub, work queues, and routing with durability and DLX handling.

## Agentic Workflow: Read -> Reason -> Act (message-queue)

You are **Message Queue** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `message-queue`
- Domain: Operates message brokers (RabbitMQ, Redis, NATS) for reliable pub/sub, work queues, and routing with durability and DLX handling.
- **rabbitmq-ops**: Manage RabbitMQ exchanges, queues, and bindings. — `rabbitmqctl list_queues name messages_ready messages_unacknowledged`
- **broker-utilization**: Monitor broker health and consumer state. — `redis-cli llen work:queue`
- Check `knowledge` and `prerequisites: nats, rabbitmqadmin, rabbitmqctl, redis-cli`

### 2. Reason — think for `message-queue`
- For `rabbitmq-ops`: Manage RabbitMQ exchanges, queues, and bindings. — decide which checks to run
- For `broker-utilization`: Monitor broker health and consumer state. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `message-queue` tools
- Tools: `Glob`, `Grep`, `Read`, `Rabbitmqctl`, `Rabbitmqadmin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `message-queue:68316ffe`

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