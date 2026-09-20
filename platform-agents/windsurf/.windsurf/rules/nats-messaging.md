---
trigger: glob
description: "Operates NATS and JetStream: pub/sub, request-reply, streams, consumers, and key-value stores. Use when working with pub sub, jetstream, messaging or when the user mentions pub sub, jetstream, messaging."
globs: ["**/*.r", "**/*.sh"]
---

Operates NATS and JetStream: pub/sub, request-reply, streams, consumers, and key-value stores.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nats sub 'orders.>'`, `nats stream add ORDERS --subjects 'orders.>' --storage file `
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

Fast, lightweight messaging with pub/sub and JetStream persistence.

## When to Use

- Microservices request-reply
- Edge and IoT messaging
- Lightweight stream processing

## Pub/sub

```bash
nats sub 'orders.>'
nats pub orders.created '{"id":1}'
```

`>` matches one or more tokens; `*` matches exactly one.

## Request-reply

```bash
nats request service.orders '{"action":"status"}'
nats reply service.orders '{"status":"ok"}'
```

## JetStream streams

```bash
nats stream add ORDERS --subjects 'orders.>' --storage file --retention limits --max-age 168h
nats stream info ORDERS
```

## Consumers

```bash
nats consumer add ORDERS order-worker --pull --deliver last --ack-explicit --max-deliver 5
nats consumer info ORDERS order-worker
```

Pull consumers are the norm for worker pools.

## KV store

```bash
nats kv add config
nats kv put config feature_flag '{"on":true}'
nats kv get config feature_flag
```

## Best practices

- Choose retention: limits (size/age), interest, or workqueue.
- Set max-deliver so poison messages end in the DLQ stream.
- Use subject naming convention: `<app>.<entity>.<action>`.
- Monitor stream lag: `nats stream report`.

## Testing

```bash
nats pub orders.created '{"id":1}' --count 1000
nats stream report ORDERS
```

Verify all 1000 land in the stream with zero loss.

## Capabilities

### pub-sub
Publish and subscribe to NATS subjects.

**Parameters:**
- `subject` (string): NATS subject with wildcards
- `payload` (string): Message payload
- `timeout` (string): Request timeout

**Commands:**
- `nats sub 'orders.>'`
- `nats pub orders.created '{"id":1}'`
- `nats request service.orders '{"action":"status"}'`
- `nats pub --reply order.ack orders.created '{"id":1}'`
- `nats reply service.orders 'ack received'`

**Examples:**
- nats sub 'metrics.>' --raw
- nats request service.health '{}' --timeout 2s
- nats pub orders.created '{"id":2}' --count 100 --sleep 0.1s

### jetstream
Manage JetStream streams, consumers, and KV.

**Parameters:**
- `stream` (string): Stream name
- `max-age` (string): Retention duration
- `storage` (string): file or memory storage

**Commands:**
- `nats stream add ORDERS --subjects 'orders.>' --storage file --retention limits --max-age 168h --max-size 10GB`
- `nats stream info ORDERS`
- `nats consumer add ORDERS order-worker --pull --deliver last --ack-explicit --max-deliver 5`
- `nats stream report ORDERS`
- `nats kv add config --history 10`

**Examples:**
- nats stream add ORDERS --subjects 'orders.>' --replicas 3
- nats consumer info ORDERS order-worker
- nats kv put config feature_flag '{"on":true}' && nats kv get config feature_flag

## References
- [NATS Docs](https://docs.nats.io/)
- [NATS CLI](https://docs.nats.io/using-nats/nats-tools/nats_cli)
- [JetStream Guide](https://docs.nats.io/nats-concepts/jetstream)
