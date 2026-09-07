---
name: "rabbitmq-quorum"
description: "RabbitMQ quorum queues: declaration, policies, durability, and replication behavior across nodes. Use when working with quorum queue operations, api or when the user mentions quorum queue operations, api."
---

RabbitMQ quorum queues: declaration, policies, durability, and replication behavior across nodes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rabbitmqadmin declare queue name=q durable=true arguments='{`
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
