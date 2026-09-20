---
type: agent_requested
description: "RabbitMQ quorum queues: declaration, policies, durability, and replication behavior across nodes. Use when working with quorum queue operations, api or when the user mentions quorum queue operations, api."
---

RabbitMQ quorum queues: declaration, policies, durability, and replication behavior across nodes.

## Agentic Workflow: Read -> Reason -> Act (rabbitmq-quorum)

You are **Rabbitmq Quorum** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rabbitmq-quorum`
- Domain: RabbitMQ quorum queues: declaration, policies, durability, and replication behavior across nodes.
- **quorum-queue-operations**: Declare quorum queues, apply HA policies and inspect queue type and replication state. — `rabbitmqadmin declare queue name=q durable=true arguments='{"x-queue-type":"quor`
- Check `knowledge` and `prerequisites: rabbitmqadmin, rabbitmqctl`

### 2. Reason — think for `rabbitmq-quorum`
- For `quorum-queue-operations`: Declare quorum queues, apply HA policies and inspect queue type and replication state. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rabbitmq-quorum` tools
- Tools: `Glob`, `Grep`, `Read`, `Rabbitmqadmin`, `Rabbitmqctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rabbitmq-quorum:c862871f`

# RabbitMQ Quorum Queues

Quorum queues replicate to multiple nodes with Raft consensus, replacing classic mirrored queues.

## What this skill does

- Declares quorum queues with arguments
- Sets HA policies
- Inspects replication and leader state

## When to use

- Durable, exactly-safe messaging
- Migrating from mirrored classic queues

## Real commands

```bash
# Declare a quorum queue
rabbitmqadmin declare queue name=orders durable=true \
  arguments='{"x-queue-type":"quorum","x-delivery-limit":5}'

# Inspect
rabbitmqctl list_queues name type messages
rabbitmqctl list_queues name node state

# Policy for quorum replication
rabbitmqctl set_policy quorum-ha "^q\." '{"ha-mode":"all"}' --apply-to queues
```

## Key facts

- Durable by design; survive broker restarts
- Leader election per queue via Raft
- Poison messages bounded by x-delivery-limit

## Best practices

- Prefer quorum queues over classic mirrored
- Set x-delivery-limit to avoid poison loops
- Use at least 3 nodes for quorum durability

## Capabilities

### quorum-queue-operations
Declare quorum queues, apply HA policies and inspect queue type and replication state.

**Parameters:**
- `queue` (string): Queue name
- `delivery_limit` (integer): Max redeliveries for quorum queues
- `policy` (string): HA policy JSON

**Commands:**
- `rabbitmqadmin declare queue name=q durable=true arguments='{"x-queue-type":"quorum"}'`
- `rabbitmqctl list_queues name type messages`
- `rabbitmqctl list_queues name policy node state`
- `rabbitmqctl set_policy quorum-ha "^q\." '{"ha-mode":"all"}' --apply-to queues`
- `rabbitmqadmin list queues name type --format=table`

**Examples:**
- rabbitmqadmin declare queue name=orders durable=true arguments='{"x-queue-type":"quorum","x-delivery-limit":5}'
- rabbitmqctl list_queues name type messages ready
- rabbitmqctl set_policy q-2 "^q\." '{"ha-mode":"exactly","ha-params":2}' --apply-to queues

## References
- [Quorum Queues Docs](https://www.rabbitmq.com/quorum-queues.html)
- [Ha Policies](https://www.rabbitmq.com/ha.html)