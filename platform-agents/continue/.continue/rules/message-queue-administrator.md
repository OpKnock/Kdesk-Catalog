---
name: "message-queue-administrator"
description: "Operates RabbitMQ and Redis Streams in production: node status, queue health, purges, and consumer troubleshooting."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

# message-queue-administrator

Operates RabbitMQ and Redis Streams in production: node status, queue health, purges, and consumer troubleshooting.

## Instructions

# Message Queue Administration

Keep queues healthy: monitor, diagnose, and recover.

## When to Use

- Queue depth alerts and stuck consumers
- Scheduled maintenance of brokers
- Debugging message loss or duplication

## RabbitMQ health

```bash
rabbitmq-diagnostics ping
rabbitmqctl status
rabbitmqctl list_connections name state
```

## Queue health

```bash
rabbitmqctl list_queues name messages messages_ready messages_unacknowledged --formatter table
```

- `messages` = total backlog
- `messages_ready` = awaiting delivery
- `messages_unacknowledged` = in-flight; if high, consumers are stuck

## Purge and reset

```bash
rabbitmqctl purge_queue dead.orders
```

Purge only after confirming the DLQ is reviewed - this is destructive.

## Redis Streams

```bash
redis-cli XLEN orders:stream
redis-cli XRANGE orders:stream - + COUNT 10
redis-cli XINFO STREAM orders:stream
redis-cli XGROUP INFO orders:stream workers
```

`pending` + `lag` in XINFO GROUPS show consumer backlog and idle time.

## Recovery playbook

1. Confirm broker is up (`rabbitmq-diagnostics ping`).
2. Check connection/consumer counts.
3. Inspect unacknowledged messages - restart stuck consumers.
4. Purge dead-letter queues only after triage.
5. Watch queue depth trend for 10 minutes after action.

## Best practices

- Alert on queue depth > threshold for > 5 minutes.
- Never purge a queue without a ticket and backup.
- Enable management plugin and lock down its network path.
- Document every queue's consumer and owner.

## Testing

```bash
rabbitmqctl list_queues name messages | wc -l
redis-cli XLEN orders:stream
```

Assert queue counts return to baseline after load tests.

## Capabilities

### rabbitmq
Administer RabbitMQ nodes and queues.

**Commands:**
- `rabbitmqctl status`
- `rabbitmqctl list_queues name messages messages_ready messages_unacknowledged --formatter table`
- `rabbitmqctl purge_queue orders`
- `rabbitmqctl list_connections name state connected_at`
- `rabbitmq-plugins enable rabbitmq_management`

**Examples:**
- rabbitmqctl list_queues name messages | sort -k2 -rn | head -10
- rabbitmqctl purge_queue dead.orders
- rabbitmq-diagnostics status --silent

### redis-streams
Inspect and manage Redis Stream consumer groups.

**Commands:**
- `redis-cli XLEN orders:stream`
- `redis-cli XADD orders:stream '*' order 1 sku A1`
- `redis-cli XRANGE orders:stream - + COUNT 10`
- `redis-cli XGROUP INFO orders:stream workers`
- `redis-cli XINFO STREAM orders:stream`

**Examples:**
- redis-cli XLEN orders:stream && redis-cli XINFO GROUPS orders:stream
- redis-cli XRANGE orders:stream - + | head -20
- redis-cli XGROUP CREATECONSUMER orders:stream workers w3