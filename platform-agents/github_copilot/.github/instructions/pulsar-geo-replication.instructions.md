---
applyTo: "**/*.r **/*.sh"
---

# Pulsar Geo Replication

Pulsar geo-replication: cluster configuration, namespace replication, and cross-region topic replication.

## Instructions

# Pulsar Geo-Replication

Geo-replication copies messages between clusters so data lives close to consumers worldwide.

## What this skill does

- Configures namespace replication across clusters
- Inspects replication state and backlog
- Troubleshoots lag between regions

## When to use

- Multi-region disaster recovery
- Global fan-out with local reads

## Real commands

```bash
# Cluster inventory
bin/pulsar-admin clusters list

# Enable replication for a namespace
bin/pulsar-admin namespaces set-clusters public/default --clusters primary,backup
bin/pulsar-admin namespaces get-clusters public/default

# Monitor replication
bin/pulsar-admin topics stats persistent://primary/my-topic | jq '.replication'
bin/pulsar-admin topics stats-internal persistent://primary/my-topic | jq '.replicationBacklog'
```

## broker.conf (both clusters)

```conf
replicationClusters=primary,backup
```

## Behavior

- Messages replicate only when both clusters in the namespace list
- Producers write locally; messages async-replicate

## Best practices

- Use persistent topics for replication
- Watch replicationBacklog per remote cluster
- Test failover by promoting the backup cluster

## Capabilities

### pulsar-geo-replication
Configure namespaces for replication across clusters and monitor replication state.

**Commands:**
- `bin/pulsar-admin clusters list`
- `bin/pulsar-admin namespaces set-clusters public/default --clusters primary,backup`
- `bin/pulsar-admin namespaces get-clusters public/default`
- `bin/pulsar-admin topics stats persistent://primary/my-topic | jq '.replication'`
- `bin/pulsar-admin topics stats-internal persistent://primary/my-topic | jq '.replicationBacklog'`

**Examples:**
- bin/pulsar-admin namespaces set-clusters public/default --clusters us-east,eu-west
- bin/pulsar-admin namespaces get-clusters public/default
- bin/pulsar-admin topics stats persistent://primary/my-topic | jq '.replicationBacklog'
