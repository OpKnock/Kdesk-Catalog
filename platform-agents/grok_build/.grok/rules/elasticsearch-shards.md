Elasticsearch shard management: inspect shard distribution and sizes, diagnose unassigned shards, and reroute shards between nodes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s 'localhost:9200/_cat/shards?v&s=index'`
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

**Parameters:**
- `index` (string): Index the shard belongs to
- `shard` (integer): Shard number
- `primary` (boolean): Whether the shard is a primary or replica

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

## References
- [Shards API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-shards.html)
- [Cluster Allocation Explain](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-allocation-explain.html)