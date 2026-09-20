---
name: "elasticsearch-cluster"
description: "Elasticsearch cluster health and operations: check node status, shard allocation, pending tasks, and cluster settings from the REST API."
---

# Elasticsearch Cluster

Elasticsearch cluster health and operations: check node status, shard allocation, pending tasks, and cluster settings from the REST API.

## Instructions

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
