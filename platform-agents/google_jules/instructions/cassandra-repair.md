# Cassandra Repair

Runs and monitors Cassandra anti-entropy repairs: full/incremental repairs, repair state, and post-repair verification.

## Instructions

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
