---
name: "nats"
description: "Publishes, subscribes, and performs request-reply over NATS subjects using the CLI. Supports wildcard patterns, queue groups enabling load balancing, and server info queries against a running instance. Use when working with nats core messaging, api or when the user mentions nats core messaging, api."
---

Publishes, subscribes, and performs request-reply over NATS subjects using the CLI. Supports wildcard patterns, queue groups enabling load balancing, and server info queries against a running instance.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nats pub orders.created '{"id":1}'`
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

# NATS

NATS is a lightweight, high-performance messaging system built around subjects and pub/sub.

## What this skill does

- Publishes and subscribes with subject wildcards
- Implements request-reply and queue groups
- Verifies server state and message flow

## When to use

- Service-to-service messaging without heavy brokers
- Fan-out events to many subscribers
- Simple RPC with request-reply

## Real commands

```bash
# Publish
nats pub orders.created '{"id":1}'
nats pub sensors.temp 21.5

# Subscribe with wildcards
nats sub 'orders.>' --all
nats sub 'orders.*' --raw

# Request-reply
nats req service.echo 'ping' --timeout 3s

# Queue group
nats subscribe 'tasks' --queue workers

# Server info
nats server info
```

## Subject rules

- `*` matches one token; `>` matches one or more at the end
- Publish permissions and queue groups are per-subject

## Patterns

- Fan-out: one publisher, many subscribers
- Load-balance: publisher + queue group of N workers
- RPC: request on subject, responders reply on inbox

## Best practices

- Design subject hierarchies before coding
- Use queue groups for competing consumers
- Set timeouts on all request-reply calls

## Capabilities

### nats-core-messaging
Publish, subscribe, request-reply and queue-group with the nats CLI against a running server.

**Parameters:**
- `subject` (string): Subject with optional wildcards
- `payload` (string): Message payload string
- `queue` (string): Queue group name for load balancing

**Commands:**
- `nats pub orders.created '{"id":1}'`
- `nats sub 'orders.>' --all`
- `nats req service.echo 'ping'`
- `nats subscribe 'tasks' --queue workers`
- `nats server info`

**Examples:**
- nats pub sensors.temp 21.5
- nats sub 'orders.*' --raw
- nats req service.echo 'hello' --timeout 3s

## References
- [NATS Documentation](https://docs.nats.io/)
- [NATS CLI Docs](https://docs.nats.io/using-nats/command-line/)
