---
trigger: glob
description: "Pulsar topic lifecycle: create partitioned/non-partitioned topics, stats, TTL/retention, and deletion. Use when working with pulsar topic lifecycle, api or when the user mentions pulsar topic lifecycle, api."
globs: ["**/*.r", "**/*.sh"]
---

Pulsar topic lifecycle: create partitioned/non-partitioned topics, stats, TTL/retention, and deletion.

## Agentic Workflow: Read -> Reason -> Act (pulsar-topics)

You are **Pulsar Topics** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-topics`
- Domain: Pulsar topic lifecycle: create partitioned/non-partitioned topics, stats, TTL/retention, and deletion.
- **pulsar-topic-lifecycle**: Manage topics: create, partition, apply retention/TTL, inspect stats and delete. — `bin/pulsar-admin topics create persistent://public/default/my-topic`
- Check `knowledge` and `prerequisites: bin/pulsar-admin`

### 2. Reason — think for `pulsar-topics`
- For `pulsar-topic-lifecycle`: Manage topics: create, partition, apply retention/TTL, inspect stats and delete. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-topics` tools
- Tools: `Glob`, `Grep`, `Read`, `Bin/pulsar-admin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-topics:4c23b91b`

# Pulsar Topics

Topics are the messaging unit in Pulsar; partitions scale them across brokers.

## What this skill does

- Creates partitioned and non-partitioned topics
- Applies retention and TTL
- Inspects stats and cleans up

## When to use

- Provisioning topics for a service
- Right-sizing partitions and retention

## Real commands

```bash
# Create
bin/pulsar-admin topics create persistent://public/default/my-topic
bin/pulsar-admin topics create-partitioned-topic persistent://public/default/my-topic -p 3

# Retention (namespace level)
bin/pulsar-admin namespaces set-retention public/default --size 10G --time 7d

# Stats
bin/pulsar-admin topics stats persistent://public/default/my-topic | jq '.msgRateIn,.storageSize'

# Truncate / delete
bin/pulsar-admin topics truncate persistent://public/default/my-topic
bin/pulsar-admin topics delete persistent://public/default/my-topic
```

## Partition sizing

- Throughput per partition ~ tens of MB/s
- Plan partitions from peak write rate and key skew

## Best practices

- Set retention before production traffic
- Monitor per-partition backlog and storage
- Use truncate for test cleanup, delete when done

## Capabilities

### pulsar-topic-lifecycle
Manage topics: create, partition, apply retention/TTL, inspect stats and delete.

**Parameters:**
- `topic` (string): Persistent topic name
- `partitions` (integer): Partition count
- `retention` (string): Retention window like 7d or size like 10G

**Commands:**
- `bin/pulsar-admin topics create persistent://public/default/my-topic`
- `bin/pulsar-admin topics create-partitioned-topic persistent://public/default/my-topic -p 3`
- `bin/pulsar-admin topics stats persistent://public/default/my-topic`
- `bin/pulsar-admin namespaces set-retention public/default --size 10G --time 7d`
- `bin/pulsar-admin topics delete persistent://public/default/my-topic`

**Examples:**
- bin/pulsar-admin topics create-partitioned-topic persistent://public/default/events -p 6
- bin/pulsar-admin topics stats persistent://public/default/events | jq '.msgRateIn,.storageSize'
- bin/pulsar-admin topics truncate persistent://public/default/events

## References
- [Pulsar Topics Concepts](https://pulsar.apache.org/docs/3.0.x/concepts-messaging/#topics)
- [pulsar-admin topics reference](https://pulsar.apache.org/docs/3.0.x/reference-pulsar-admin-topics/)
