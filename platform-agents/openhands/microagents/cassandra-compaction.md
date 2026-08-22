---
name: "cassandra-compaction"
description: "Monitors and controls SSTable merging in Apache Cassandra: inspects compactionstats and history, triggers manual merges, stops runaway operations, and selects or tunes strategies (STCS, LCS, TWCS) for table behavior."
type: knowledge
triggers: ["cassandra-compaction", "compaction-status", "manual-compaction", "strategy-tuning"]
---

# Cassandra Compaction

Monitors and controls SSTable merging in Apache Cassandra: inspects compactionstats and history, triggers manual merges, stops runaway operations, and selects or tunes strategies (STCS, LCS, TWCS) for table behavior.

## Instructions

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
