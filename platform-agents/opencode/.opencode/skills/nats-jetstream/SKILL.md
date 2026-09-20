---
name: "nats-jetstream"
description: "NATS JetStream core: create streams, message retention, storage engines, and durability configuration. Use when working with jetstream streams, api or when the user mentions jetstream streams, api."
---

NATS JetStream core: create streams, message retention, storage engines, and durability configuration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nats server check jetstream`
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

# NATS JetStream

JetStream adds durable streams and consumer groups to NATS, enabling reliable messaging.

## What this skill does

- Verifies JetStream is enabled on the server
- Creates streams with subjects and retention policies
- Publishes to and reads from streams

## When to use

- Persisting events for replay
- Exactly-once-capable event processing
- Replacing Kafka-style messaging with NATS

## Real commands

```bash
# Verify JetStream is running
nats server check jetstream

# Create a stream
nats stream add ORDERS --subjects 'orders.*' --storage file
nats stream add EVENTS --subjects 'events.>' --retention limits --max-age 24h

# List and inspect
nats stream ls
nats stream info ORDERS

# Purge and delete
nats stream purge ORDERS --force
nats stream rm ORDERS
```

## Publish into a stream

```bash
nats pub orders.created '{"id":1}' --stream ORDERS
nats stream view ORDERS
```

## Retention policies

- `limits`: keep until limits hit (default)
- `interest`: drop when all consumers have seen them
- `workqueue`: single consumer, delete on ack

## Best practices

- Use file storage for durable data, memory for cache-like streams
- Set max-age/max-bytes to bound disk
- Always name streams clearly and match subjects deliberately

## Capabilities

### jetstream-streams
Create and manage JetStream streams, configure retention/storage, and produce/consume messages.

**Parameters:**
- `stream` (string): Stream name
- `subjects` (array): Subject filters the stream captures
- `retention` (string): limits, interest or workqueue

**Commands:**
- `nats server check jetstream`
- `nats stream add ORDERS --subjects 'orders.*' --storage file`
- `nats stream ls`
- `nats stream info ORDERS`
- `nats stream rm ORDERS`

**Examples:**
- nats stream add EVENTS --subjects 'events.>' --retention limits --max-age 24h --storage file
- nats stream info ORDERS
- nats stream purge ORDERS --force

## References
- [NATS JetStream Concepts](https://docs.nats.io/nats-concepts/jetstream)
- [nats CLI reference](https://docs.nats.io/using-nats/command-line/)
