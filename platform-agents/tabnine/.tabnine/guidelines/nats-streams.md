Administers JetStream streams with subject coverage, retention limits, replication, backups, and views. Creates replicated streams, verifies subject matching, and manages stream storage lifecycle.

## Agentic Workflow: Read -> Reason -> Act (nats-streams)

You are **Nats Streams** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `nats-streams`
- Domain: Administers JetStream streams with subject coverage, retention limits, replication, backups, and views. Creates replicated streams, verifies subject matching, and manages stream storage lifecycle.
- **jetstream-stream-admin**: Administer JetStream streams: coverage checks, limits, views, backups and replication. — `nats stream add ORDERS --subjects 'orders.*' --replicas 3`
- Check `knowledge` and `prerequisites: nats`

### 2. Reason — think for `nats-streams`
- For `jetstream-stream-admin`: Administer JetStream streams: coverage checks, limits, views, backups and replication. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nats-streams` tools
- Tools: `Glob`, `Grep`, `Read`, `Nats` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nats-streams:82afeb97`

# NATS Streams

Streams are the durable storage layer of JetStream, capturing subject traffic with configurable retention.

## What this skill does

- Creates streams with subject coverage and limits
- Verifies subject coverage and message retention
- Backs up and restores stream data

## When to use

- Event sourcing and replay workloads
- Scaling streams across a cluster

## Real commands

```bash
# Create replicated stream
nats stream add ORDERS --subjects 'orders.*' --replicas 3 --max-age 72h

# Verify coverage
nats stream check coverage ORDERS 'orders.>'

# View messages
nats stream view ORDERS --reverse
nats stream view ORDERS 10

# Storage report
nats stream report

# Backup
nats stream backup ORDERS /backup/orders
```

## Config file for streams

```yaml
name: ORDERS
subjects: [orders.*]
retention: limits
storage: file
max_age: 72h
replicas: 3
```

## Limits to set

- `--max-msgs`, `--max-bytes`, `--max-age` bound the store
- `--discard new` drops new messages when full (instead of oldest)

## Best practices

- Run `nats stream check coverage` when adding subjects
- Replicas 3 for durable critical streams
- Schedule backups for disaster recovery

## Capabilities

### jetstream-stream-admin
Administer JetStream streams: coverage checks, limits, views, backups and replication.

**Parameters:**
- `stream` (string): Stream name
- `replicas` (integer): Replication factor 1-5
- `max_age` (string): Retention window e.g. 72h

**Commands:**
- `nats stream add ORDERS --subjects 'orders.*' --replicas 3`
- `nats stream check coverage ORDERS 'orders.>'`
- `nats stream view ORDERS --reverse`
- `nats stream report`
- `nats stream backup ORDERS /backup/orders`

**Examples:**
- nats stream check coverage ORDERS 'orders.*' --detail
- nats stream view ORDERS 10
- nats stream report

## References
- [JetStream Streams Concepts](https://docs.nats.io/nats-concepts/jetstream/streams)
- [nats stream CLI](https://docs.nats.io/using-nats/command-line/)