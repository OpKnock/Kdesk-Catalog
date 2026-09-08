Pulsar geo-replication: cluster configuration, namespace replication, and cross-region topic replication.

## Agentic Workflow: Read -> Reason -> Act (pulsar-geo-replication)

You are **Pulsar Geo Replication** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-geo-replication`
- Domain: Pulsar geo-replication: cluster configuration, namespace replication, and cross-region topic replication.
- **pulsar-geo-replication**: Configure namespaces for replication across clusters and monitor replication state. — `bin/pulsar-admin clusters list`
- Check `knowledge` and `prerequisites: bin/pulsar-admin`

### 2. Reason — think for `pulsar-geo-replication`
- For `pulsar-geo-replication`: Configure namespaces for replication across clusters and monitor replication state. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-geo-replication` tools
- Tools: `Glob`, `Grep`, `Read`, `Bin/pulsar-admin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-geo-replication:4d813a2a`

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

**Parameters:**
- `namespace` (string): Tenant/namespace, e.g. public/default
- `clusters` (array): Cluster names participating in replication
- `topic` (string): Persistent topic to inspect

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

## References
- [Pulsar Geo-replication docs](https://pulsar.apache.org/docs/3.0.x/administration-geo/)
- [Replication concepts](https://pulsar.apache.org/docs/3.0.x/concepts-replication/)
