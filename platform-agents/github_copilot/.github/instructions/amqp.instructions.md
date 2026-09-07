---
applyTo: "**/*.r **/*.sh"
---

Operates AMQP brokers (RabbitMQ) with rabbitmqctl and rabbitmqadmin: queue/exchange inspection, message publish/get, and user management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rabbitmqctl status`, `rabbitmqadmin declare queue name=orders durable=true`
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

# AMQP

## What this skill does

Operates AMQP brokers with RabbitMQ tooling: inspecting queues/exchanges/bindings, managing users and permissions, publishing and consuming test messages, and troubleshooting delivery.

## When to use

- Messages pile up in a queue and consumers are idle
- Setting up an exchange topology for events
- Debugging redelivery, unacked messages, or routing misses

## Real commands

```bash
# Status and queues
rabbitmqctl status
rabbitmqctl list_queues name messages messages_ready messages_unacknowledged

# Exchanges and bindings
rabbitmqadmin list exchanges name type
rabbitmqctl list_bindings source_name destination_name routing_key

# Publish and consume test messages
rabbitmqadmin publish exchange=events routing_key=order.created payload='{"id":1}'
rabbitmqadmin get queue=orders count=5

# Purge a stuck queue
rabbitmqctl purge_queue orders

# Users
rabbitmqctl add_user svc-user secret123
rabbitmqctl set_permissions -p / svc-user ".*" ".*" ".*"
```

## Common failure patterns

- messages_unacknowledged high: consumer died mid-processing
- Routing misses: binding key does not match routing key pattern
- Publisher confirms: enable in clients for durability

## Testing

- Use rabbitmqadmin publish/get as a black-box smoke test
- Verify auth with `rabbitmqctl authenticate_user <user> <pass>`

## Best practices

- Grant least-privilege regexes per vhost
- Monitor messages_ready/unacknowledged with alerts
- Prefer dead-letter queues over purge_queue

## Capabilities

### broker-ops
Inspect broker status, queues, exchanges, and bindings.

**Parameters:**
- `vhost` (string): Virtual host filter, e.g. /api
- `queue` (string): Queue name to inspect

**Commands:**
- `rabbitmqctl status`
- `rabbitmqctl list_queues name messages consumers`
- `rabbitmqadmin list exchanges name type`
- `rabbitmqctl list_bindings`
- `rabbitmqctl list_channels`

**Examples:**
- rabbitmqctl list_queues name messages messages_ready messages_unacknowledged
- rabbitmqadmin list queues vhost name messages -f table
- rabbitmqctl list_exchanges name type durable

### queue-management
Declare, purge, delete queues and publish/consume for debugging.

**Parameters:**
- `routing_key` (string): Routing key for topic exchanges
- `payload` (string): Message body to publish
- `count` (number): Number of messages to fetch

**Commands:**
- `rabbitmqadmin declare queue name=orders durable=true`
- `rabbitmqadmin declare exchange name=events type=topic`
- `rabbitmqadmin publish exchange=events routing_key=order.created payload='{"id":1}'`
- `rabbitmqadmin get queue=orders count=10 requeue=false`
- `rabbitmqctl purge_queue orders`

**Examples:**
- rabbitmqadmin publish exchange=events routing_key=order.created payload='hello' -u guest -p guest
- rabbitmqadmin get queue=orders count=5
- rabbitmqctl purge_queue orders -p /api

### user-management
Manage AMQP users and permissions across vhosts.

**Parameters:**
- `user` (string): RabbitMQ username
- `vhost` (string): Vhost to grant permissions on
- `permissions` (string): Configure-write-read regex triple

**Commands:**
- `rabbitmqctl add_user svc-user secret123`
- `rabbitmqctl set_permissions -p / svc-user ".*" ".*" ".*"`
- `rabbitmqctl list_users`
- `rabbitmqctl delete_user svc-user`
- `rabbitmqctl change_password svc-user newsecret`

**Examples:**
- rabbitmqctl set_permissions -p /api svc-user "^orders.*" ".*" ".*"
- rabbitmqctl list_permissions -p /
- rabbitmqctl authenticate_user svc-user secret123

## References
- [RabbitMQ Docs](https://www.rabbitmq.com/docs)
- [rabbitmqctl](https://www.rabbitmq.com/docs/man/rabbitmqctl.8)
- [rabbitmqadmin](https://www.rabbitmq.com/docs/management-cli)
- [AMQP Concepts](https://www.rabbitmq.com/tutorials/amqp-concepts)
