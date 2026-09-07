---
type: agent_requested
description: "Pulsar geo-replication: cluster configuration, namespace replication, and cross-region topic replication. Use when working with pulsar geo replication, api or when the user mentions pulsar geo replication, api."
---

Pulsar geo-replication: cluster configuration, namespace replication, and cross-region topic replication.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bin/pulsar-admin clusters list`
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