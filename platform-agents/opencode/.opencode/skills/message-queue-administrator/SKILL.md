---
name: "message-queue-administrator"
description: "Operates RabbitMQ and Redis Streams in production: node status, queue health, purges, and consumer troubleshooting. Use when working with rabbitmq, redis streams or when the user mentions rabbitmq, redis streams."
---

Operates RabbitMQ and Redis Streams in production: node status, queue health, purges, and consumer troubleshooting.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rabbitmqctl status`, `redis-cli XLEN orders:stream`
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

**Parameters:**
- `queue` (string): Queue name for purge/list
- `formatter` (string): table, tsv, or json output
- `plugin` (string): rabbitmq plugin to enable

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

**Parameters:**
- `stream` (string): Stream key name
- `group` (string): Consumer group name
- `count` (number): Number of entries to return

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

## References
- [RabbitMQ CLI](https://www.rabbitmq.com/docs/cli)
- [RabbitMQ Management](https://www.rabbitmq.com/docs/management)
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)
