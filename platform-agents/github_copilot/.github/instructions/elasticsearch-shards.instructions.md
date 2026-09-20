---
applyTo: "**/*.json **/*.r **/*.sh"
---

# Elasticsearch Shards

Elasticsearch shard management: inspect shard distribution and sizes, diagnose unassigned shards, and reroute shards between nodes.

## Instructions

# Elasticsearch Shards

## What this skill does

This skill focuses on shards: where they sit, how big they are, why they are unassigned, and how to move them. The cat APIs give instant table views; allocation explain gives reasons.

## When to use

- Investigating UNASSIGNED shards after hardware changes
- Rebalancing hot shards onto idle nodes
- Right-sizing index shard counts

## Real commands

```bash
# Shard table: state, docs, size, node
curl -s 'localhost:9200/_cat/shards?v&h=index,shard,prirep,state,docs,store,node&s=store:desc'

# Only unassigned
curl -s 'localhost:9200/_cat/shards?v&h=index,shard,prirep,state,store,node' | grep UNASSIGNED

# Why can't this shard allocate?
curl -s 'localhost:9200/_cluster/allocation/explain?pretty' -H 'Content-Type: application/json' -d '{"index":"logs-2024.01","shard":2,"primary":false}' | jq '.can_allocate, .allocate_explanation'

# Manually move a shard
curl -s -X POST 'localhost:9200/_cluster/reroute' -H 'Content-Type: application/json' -d '{"commands":[{"move":{"index":"logs-2024.01","shard":2,"from_node":"node-a","to_node":"node-b"}}]}' | jq
```

## Index sizing rule of thumb

- Keep primary shards between 10-50 GB each.
- Total shards across the cluster: about 20-40 per GB of heap (with defaults).
- Use one primary per index per shard-count check: `_cat/shards | wc -l`.

## Reroute safety

```bash
# Check allocation explain BEFORE any manual move
curl -s 'localhost:9200/_cluster/allocation/explain?pretty' -H 'Content-Type: application/json' -d '{}' | jq '.explanation'
```

## Best practices

- Let the allocator do the work; only reroute manually in emergencies.
- Watch `relocating_shards` in health before triggering further moves.
- Prefer ILM rollovers over adding shards to a growing index.
- Track shard sizes with `s=store:desc` to find oversized indices.

## Capabilities

### shard-management
List shard state and sizes, explain unassigned shards, and manually reroute shards.

**Commands:**
- `curl -s 'localhost:9200/_cat/shards?v&s=index'`
- `curl -s 'localhost:9200/_cat/shards?v&h=index,shard,prirep,state,docs,store,node&s=store:desc'`
- `curl -s 'localhost:9200/_cluster/allocation/explain?pretty' -H 'Content-Type: application/json' -d '{"index":"logs-2024.01","shard":2,"primary":false}' | jq '.can_allocate, .allocate_explanation'`
- `curl -s -X POST 'localhost:9200/_cluster/reroute' -H 'Content-Type: application/json' -d '{"commands":[{"move":{"index":"logs-2024.01","shard":2,"from_node":"node-a","to_node":"node-b"}}]}' | jq`
- `curl -s 'localhost:9200/_cat/indices?v&s=pri.store.size:desc' | head -20`

**Examples:**
- curl -s 'localhost:9200/_cat/shards?v&h=index,shard,prirep,state,store,node' | grep UNASSIGNED
- curl -s 'localhost:9200/_cluster/allocation/explain?pretty' -H 'Content-Type: application/json' -d '{"index":"logs-2024.01","shard":2,"primary":false}' | jq '.allocate_explanation'
- curl -s 'localhost:9200/_cat/shards?v&s=store:desc' | head -15
