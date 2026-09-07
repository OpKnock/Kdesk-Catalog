---
applyTo: "**/*.r **/*.sh"
---

Core Pulsar operations: standalone cluster, topics, admin APIs, producers/consumers and messaging concepts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bin/pulsar standalone`
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
