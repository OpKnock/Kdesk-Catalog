---
name: "pulsar"
description: "Core Pulsar operations: standalone cluster, topics, admin APIs, producers/consumers and messaging concepts."
---

# Pulsar

Core Pulsar operations: standalone cluster, topics, admin APIs, producers/consumers and messaging concepts.

## Instructions

# Pulsar

Apache Pulsar is a multi-tenant pub/sub and streaming platform with per-topic backpressure and geo-replication.

## What this skill does

- Runs a standalone cluster for dev
- Creates and inspects topics
- Produces/consumes via CLI tools

## When to use

- Evaluating or adopting Pulsar
- Day-to-day topic operations

## Real commands

```bash
# Standalone cluster
bin/pulsar standalone

# Topic management
bin/pulsar-admin topics create persistent://public/default/my-topic
bin/pulsar-admin topics list public/default
bin/pulsar-admin topics create-partitioned-topic persistent://public/default/my-topic -p 3

# Produce / consume
bin/pulsar-client produce my-topic --messages "Hello World"
bin/pulsar-client consume my-topic -s my-sub --num-messages 5
```

## Concepts

- Topic: persistent://tenant/namespace/topic
- Subscription: cursor over a topic (Exclusive/Shared/Failover/Key_Shared)
- Broker + BookKeeper: serving and storage split

## Best practices

- Use persistent topics for durable workloads
- Partition topics before heavy traffic
- Manage via pulsar-admin, not ad-hoc scripts

## Capabilities

### pulsar-core-operations
Run a standalone Pulsar, manage topics, and produce/consume messages via the CLI tools.

**Commands:**
- `bin/pulsar standalone`
- `bin/pulsar-admin topics create persistent://public/default/my-topic`
- `bin/pulsar-client produce my-topic --messages "Hello World"`
- `bin/pulsar-client consume my-topic -s my-sub --num-messages 5`
- `bin/pulsar-admin topics list public/default`

**Examples:**
- bin/pulsar standalone --num-brokers 2
- bin/pulsar-admin topics create-partitioned-topic persistent://public/default/my-topic -p 3
- bin/pulsar-client produce my-topic --messages "one" "two" "three" -n 1
