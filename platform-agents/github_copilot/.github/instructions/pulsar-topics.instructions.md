---
applyTo: "**/*.r **/*.sh"
---

# Pulsar Topics

Pulsar topic lifecycle: create partitioned/non-partitioned topics, stats, TTL/retention, and deletion.

## Instructions

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
