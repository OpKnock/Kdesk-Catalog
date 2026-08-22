---
name: "rabbitmq-quorum"
description: "RabbitMQ quorum queues: declaration, policies, durability, and replication behavior across nodes."
type: knowledge
triggers: ["rabbitmq-quorum", "quorum-queue-operations"]
---

# Rabbitmq Quorum

RabbitMQ quorum queues: declaration, policies, durability, and replication behavior across nodes.

## Instructions

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
