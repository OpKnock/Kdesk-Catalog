---
name: "cassandra-repair"
description: "Runs and monitors Cassandra anti-entropy repairs: full/incremental repairs, repair state, and post-repair verification. Use when working with run repair, repair status, verification, api or when the user mentions run repair, repair status, verification, api."
type: knowledge
triggers: ["cassandra-repair", "run-repair", "repair-status", "verification"]
---

Runs and monitors Cassandra anti-entropy repairs: full/incremental repairs, repair state, and post-repair verification.

## Agentic Workflow: Read -> Reason -> Act (cassandra-repair)

You are **Cassandra Repair** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `cassandra-repair`
- Domain: Runs and monitors Cassandra anti-entropy repairs: full/incremental repairs, repair state, and post-repair verification.
- **run-repair**: Execute and schedule repairs. — `nodetool repair -pr`
- **repair-status**: Monitor repair state and consistency. — `nodetool repair -pr -st $(date -d '1 hour ago' +%s000) mykeyspace`
- **verification**: Verify consistency after repair. — `cqlsh -e "CONSISTENCY QUORUM"`
- Check `knowledge` and `prerequisites: cqlsh, nodetool`

### 2. Reason — think for `cassandra-repair`
- For `run-repair`: Execute and schedule repairs. — decide which checks to run
- For `repair-status`: Monitor repair state and consistency. — decide which checks to run
- For `verification`: Verify consistency after repair. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cassandra-repair` tools
- Tools: `Glob`, `Grep`, `Read`, `Nodetool`, `Cqlsh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cassandra-repair:cbabe052`

# Cassandra Repair

## What this skill does

Runs anti-entropy repairs: primary-range (incremental) and full repairs, datacenter-scoped repairs, monitoring stream rates, and verifying consistency afterward.

## When to use

- Detected drift between replicas (inconsistency)
- Routine maintenance (weekly incremental, monthly full)
- After node additions/removals

## Real commands

```bash
# Primary-range repair (recommended default)
nodetool repair -pr

# Full repair of one keyspace
nodetool repair -full mykeyspace

# Table-scoped
nodetool repair -pr mykeyspace users

# Datacenter-scoped
nodetool repair -pr -dc dc1 mykeyspace

# Monitor
nodetool netstats | grep -E 'Repair|Streaming'
nodetool status -r
```

## Scheduling

- Run repairs from a dedicated node, not app nodes
- Incremental repairs daily; full repairs monthly

## Testing

- Verify QUORUM reads return consistent counts after repair
- Check nodetool status shows UN for all nodes

## Best practices

- Run repairs off-peak with stream throttling
- Monitor repair duration and failure rates
- Always run -pr to avoid overlapping repairs

## Capabilities

### run-repair
Execute and schedule repairs.

**Parameters:**
- `keyspace` (string): Keyspace to repair
- `table` (string): Table to repair
- `dc` (string): Datacenter filter

**Commands:**
- `nodetool repair -pr`
- `nodetool repair -full mykeyspace`
- `nodetool repair -pr mykeyspace users`
- `nodetool repair -pr -dc dc1 mykeyspace`
- `nodetool repair -pr --parallelism parallel mykeyspace`

**Examples:**
- nodetool repair -pr mykeyspace users
- nodetool repair -full mykeyspace
- nodetool repair -pr -dc dc1 dc2 mykeyspace

### repair-status
Monitor repair state and consistency.

**Parameters:**
- `start_time` (string): Repair range start (ms epoch)
- `end_time` (string): Repair range end (ms epoch)

**Commands:**
- `nodetool repair -pr -st $(date -d '1 hour ago' +%s000) mykeyspace`
- `nodetool netstats`
- `nodetool status`
- `nodetool getstreamthroughput`
- `nodetool tpstats | grep -E 'REPAIR|Repair'`

**Examples:**
- nodetool netstats | grep -E 'Repair|Streaming'
- nodetool status | grep -E 'UN|DN'
- nodetool tpstats | grep Repair

### verification
Verify consistency after repair.

**Parameters:**
- `consistency` (string): Consistency level for verification reads
- `partition_key` (string): PK to check endpoints for

**Commands:**
- `cqlsh -e "CONSISTENCY QUORUM"`
- `nodetool status -r`
- `nodetool describecluster`
- `nodetool getendpoints mykeyspace users 42`
- `cqlsh -e "SELECT COUNT(*) FROM mykeyspace.users"`

**Examples:**
- nodetool status -r
- nodetool getendpoints mykeyspace users 42
- cqlsh -e "CONSISTENCY QUORUM; SELECT COUNT(*) FROM mykeyspace.users"

## References
- [Cassandra Repair](https://cassandra.apache.org/doc/latest/cassandra/operating/repair.html)
- [nodetool Reference](https://cassandra.apache.org/doc/latest/cassandra/operating/nodetool/)
- [Repair Strategies](https://thelastpickle.com/blog/2017/09/18/repairs-in-cassandra.html)
