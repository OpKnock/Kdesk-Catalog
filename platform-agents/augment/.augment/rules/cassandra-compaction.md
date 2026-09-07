---
type: agent_requested
description: "Monitors and controls SSTable merging in Apache Cassandra: inspects compactionstats and history, triggers manual merges, stops runaway operations, and selects or tunes strategies (STCS, LCS, TWCS) for table behavior. Use when working with compaction status, manual compaction, strategy tuning, api or when the user mentions compaction status, manual compaction, strategy tuning, api."
---

Monitors and controls SSTable merging in Apache Cassandra: inspects compactionstats and history, triggers manual merges, stops runaway operations, and selects or tunes strategies (STCS, LCS, TWCS) for table behavior.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nodetool compactionstats`, `nodetool compact mykeyspace users`
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

# Cassandra Compaction

## What this skill does

Manages Cassandra compaction: monitoring activity with compactionstats, triggering manual compactions, stopping runaway compaction, and selecting/tuning strategies (STCS/LCS/TWCS).

## When to use

- Disk usage climbs due to many small SSTables
- Compaction is starving the cluster of I/O
- Choosing the right strategy for a table's workload

## Real commands

```bash
# Monitor
nodetool compactionstats
nodetool compactionhistory | tail -20

# Manual compaction
nodetool compact mykeyspace users

# Stop runaway compaction
nodetool stop compaction

# Flush memtables first if needed
nodetool flush mykeyspace users

# Set strategy via cqlsh
cqlsh -e "ALTER TABLE mykeyspace.users WITH compaction = {'class':'LeveledCompactionStrategy','sstable_size_in_mb':160}"

# Throttle
nodetool setcompactionthroughput 64
```

## Strategy guidance

- STCS: default; good for most workloads
- LCS: read-heavy, low-latency (better read amplification)
- TWCS: time-series with TTL data

## Testing

- Check compactionhistory for completed runs after manual compact
- Watch pending tasks in compactionstats

## Best practices

- Schedule major compactions in maintenance windows
- Throttle during peak traffic
- Use TWCS for time-series tables; never LCS+TWCS mix

## Capabilities

### compaction-status
Inspect compaction activity and history.

**Parameters:**
- `keyspace` (string): Keyspace name
- `table` (string): Table name

**Commands:**
- `nodetool compactionstats`
- `nodetool compactionhistory`
- `nodetool status`
- `nodetool cfstats mykeyspace`
- `nodetool tablestats mykeyspace.users`

**Examples:**
- nodetool compactionstats
- nodetool compactionhistory | tail -20
- nodetool tablestats mykeyspace.users | grep -E 'SSTable|pending'

### manual-compaction
Trigger or stop compaction on tables.

**Parameters:**
- `keyspace` (string): Keyspace to compact
- `table` (string): Table to compact

**Commands:**
- `nodetool compact mykeyspace users`
- `nodetool compact -- mykeyspace users`
- `nodetool stop compaction`
- `nodetool scrub mykeyspace users`
- `nodetool flush mykeyspace users`

**Examples:**
- nodetool compact mykeyspace users
- nodetool stop compaction
- nodetool flush mykeyspace users

### strategy-tuning
Set and tune compaction strategies.

**Parameters:**
- `strategy` (string): STCS, LCS, TWCS
- `throughput` (number): Compaction throughput MB/s

**Commands:**
- `cqlsh -e "ALTER TABLE mykeyspace.users WITH compaction = {'class':'LeveledCompactionStrategy','sstable_size_in_mb':160}"`
- `cqlsh -e "SELECT table_name, compaction FROM system_schema.tables WHERE keyspace_name='mykeyspace'"`
- `cqlsh -e "ALTER TABLE mykeyspace.users WITH compaction = {'class':'SizeTieredCompactionStrategy','min_threshold':4}"`
- `nodetool getcompactionthroughput`
- `nodetool setcompactionthroughput 64`

**Examples:**
- cqlsh -e "ALTER TABLE mykeyspace.users WITH compaction = {'class':'LeveledCompactionStrategy','sstable_size_in_mb':160}"
- cqlsh -e "SELECT table_name, compaction FROM system_schema.tables WHERE keyspace_name='mykeyspace'"
- nodetool setcompactionthroughput 64

## References
- [Cassandra Compaction](https://cassandra.apache.org/doc/latest/cassandra/operating/compaction/index.html)
- [nodetool Reference](https://cassandra.apache.org/doc/latest/cassandra/operating/nodetool/)