---
applyTo: "**/*.json **/*.r **/*.sh"
---

Elasticsearch cluster health and operations: check node status, shard allocation, pending tasks, and cluster settings from the REST API.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s 'localhost:9200/_cluster/health?pretty' | jq`
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

# Elasticsearch Cluster

## What this skill does

This skill is about the Elasticsearch cluster as a whole: node state, shard allocation, disk pressure, pending tasks, and cluster-wide settings. You operate the cluster via the REST API with curl and jq.

## When to use

- A cluster turns yellow or red
- Nodes show high disk or heap pressure
- Shards are unassigned after a node restart

## Real commands

```bash
# Overall status
curl -s 'localhost:9200/_cluster/health?pretty' | jq '{status, unassigned_shards, number_of_nodes, active_shards_percent_as_number}'

# Node inventory: heap, disk, master eligibility
curl -s 'localhost:9200/_cat/nodes?v&h=name,heap.percent,disk.used_percent,master,node.role'

# Disk allocation per node
curl -s 'localhost:9200/_cat/allocation?v&s=disk.percent:desc'

# Why are shards unassigned?
curl -s 'localhost:9200/_cluster/reroute?explain' | jq '.explanations[].deciders'

# Cluster settings (persistent vs transient)
curl -s 'localhost:9200/_cluster/settings?include_defaults=true' | jq '.persistent'
```

## Status meaning

- green: all primary and replica shards allocated
- yellow: primaries allocated, replicas missing (e.g. one node)
- red: at least one primary unassigned - data at risk

## Common fixes

```bash
# Set a watermark and reroute with retries
curl -s -X PUT 'localhost:9200/_cluster/settings' -H 'Content-Type: application/json' -d '{"persistent":{"cluster.routing.allocation.disk.watermark.high":"85%"}}' | jq

# Retry failed allocations
curl -s -X POST 'localhost:9200/_cluster/reroute?retry_failed=true' | jq
```

## Best practices

- Alert on yellow for more than 5 minutes and red immediately.
- Keep disk below 80%; watch `_cat/allocation` sorted by percent.
- Prefer `retry_failed=true` over manual shard moves.
- Never set transient settings in automation; use persistent.

## Capabilities

### cluster-health
Inspect cluster health, nodes, allocations, and settings; diagnose red/yellow cluster states.

**Parameters:**
- `es-url` (string): Elasticsearch endpoint (default localhost:9200)
- `timeout` (string): Wait-for-status timeout like 50s for health checks
- `level` (string): Health detail level: cluster, indices, shards

**Commands:**
- `curl -s 'localhost:9200/_cluster/health?pretty' | jq`
- `curl -s 'localhost:9200/_cat/nodes?v'`
- `curl -s 'localhost:9200/_cat/allocation?v&s=disk.percent:desc'`
- `curl -s 'localhost:9200/_cluster/pending_tasks?pretty'`
- `curl -s 'localhost:9200/_cluster/settings?include_defaults=true' | jq '.persistent'`

**Examples:**
- curl -s 'localhost:9200/_cluster/health?pretty' | jq '{status, unassigned_shards, number_of_nodes}'
- curl -s 'localhost:9200/_cat/nodes?v&h=name,heap.percent,disk.used_percent,master'
- curl -s 'localhost:9200/_cluster/reroute?explain' | jq

## References
- [Cluster Health API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-health.html)
- [Cluster Settings API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-update-settings.html)
