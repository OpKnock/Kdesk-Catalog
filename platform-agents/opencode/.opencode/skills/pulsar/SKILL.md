---
name: "pulsar"
description: "Core Pulsar operations: standalone cluster, topics, admin APIs, producers/consumers and messaging concepts. Use when working with pulsar core operations, api or when the user mentions pulsar core operations, api."
---

Core Pulsar operations: standalone cluster, topics, admin APIs, producers/consumers and messaging concepts.

## Agentic Workflow: Read -> Reason -> Act (pulsar)

You are **Pulsar** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar`
- Domain: Core Pulsar operations: standalone cluster, topics, admin APIs, producers/consumers and messaging concepts.
- **pulsar-core-operations**: Run a standalone Pulsar, manage topics, and produce/consume messages via the CLI tools. — `bin/pulsar standalone`
- Check `knowledge` and `prerequisites: bin/pulsar, bin/pulsar-admin, bin/pulsar-client`

### 2. Reason — think for `pulsar`
- For `pulsar-core-operations`: Run a standalone Pulsar, manage topics, and produce/consume messages via the CLI tools. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar` tools
- Tools: `Glob`, `Grep`, `Read`, `Bin/pulsar`, `Bin/pulsar-admin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar:87539a0c`

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

**Parameters:**
- `topic` (string): Persistent topic name
- `subscription` (string): Subscription name
- `num_messages` (integer): Messages to consume

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

## References
- [Apache Pulsar Docs](https://pulsar.apache.org/docs/)
- [Pulsar CLI tools](https://pulsar.apache.org/docs/3.0.x/reference-cli-tools/)
