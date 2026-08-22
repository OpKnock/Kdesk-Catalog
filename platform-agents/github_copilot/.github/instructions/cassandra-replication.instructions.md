---
applyTo: "**/*.go **/*.r **/*.sh"
---

# Cassandra Replication

Manages Cassandra replication: replication factors, keyspace strategies, endpoint mapping, and consistency levels.

## Instructions

# Cassandra Replication

## What this skill does

Manages Cassandra replication: setting replication factors per datacenter, mapping partition keys to replicas, and testing consistency levels with tracing.

## When to use

- Adding a datacenter or changing RF
- Debugging 'unavailable' errors
- Understanding which nodes hold a partition

## Real commands

```bash
# Inspect replication
cqlsh -e "DESCRIBE KEYSPACE mykeyspace"
cqlsh -e "SELECT keyspace_name, replication FROM system_schema.keyspaces"

# Change RF
cqlsh -e "ALTER KEYSPACE mykeyspace WITH replication = {'class':'NetworkTopologyStrategy','dc1':3,'dc2':3}"

# Map a key to replicas
nodetool getendpoints mykeyspace users 42

# Test consistency
cqlsh -e "CONSISTENCY QUORUM; SELECT COUNT(*) FROM mykeyspace.users"
cqlsh -e "TRACING ON; SELECT * FROM mykeyspace.users WHERE id=42"
```

## RF and CL math

- QUORUM = (RF/2) + 1 per DC (LOCAL_QUORUM)
- For RF=3: QUORUM needs 2 replicas
- EACH_QUORUM: quorum in every DC

## Testing

- getendpoints shows expected replica count = RF
- Trace queries to see contact points and read repair

## Best practices

- Use NetworkTopologyStrategy in production
- Run nodetool repair after RF changes
- Prefer LOCAL_QUORUM over QUORUM in multi-DC

## Capabilities

### keyspace-replication
Set and inspect replication configuration.

**Commands:**
- `cqlsh -e "DESCRIBE KEYSPACE mykeyspace"`
- `cqlsh -e "ALTER KEYSPACE mykeyspace WITH replication = {'class':'NetworkTopologyStrategy','dc1':3,'dc2':3}"`
- `cqlsh -e "SELECT keyspace_name, replication FROM system_schema.keyspaces"`
- `cqlsh -e "CREATE KEYSPACE mykeyspace WITH replication = {'class':'NetworkTopologyStrategy','dc1':3}"`
- `cqlsh -e "SELECT keyspace_name, replication, durable_writes FROM system_schema.keyspaces WHERE keyspace_name='mykeyspace'"`

**Examples:**
- cqlsh -e "ALTER KEYSPACE mykeyspace WITH replication = {'class':'NetworkTopologyStrategy','dc1':3,'dc2':3}"
- cqlsh -e "SELECT keyspace_name, replication FROM system_schema.keyspaces"
- cqlsh -e "CREATE KEYSPACE app WITH replication = {'class':'SimpleStrategy','replication_factor':2}"

### endpoints
Map partition keys to replicas.

**Commands:**
- `nodetool getendpoints mykeyspace users 42`
- `nodetool status`
- `nodetool status -r`
- `nodetool gossipinfo`
- `nodetool ring | grep -E 'dc1|dc2'`

**Examples:**
- nodetool getendpoints mykeyspace users 42
- nodetool ring | head -20
- nodetool status -r

### consistency
Set and test consistency levels.

**Commands:**
- `cqlsh -e "CONSISTENCY QUORUM"`
- `cqlsh -e "CONSISTENCY LOCAL_QUORUM"`
- `cqlsh -e "CONSISTENCY ONE; SELECT COUNT(*) FROM mykeyspace.users"`
- `cqlsh -e "TRACING ON; SELECT * FROM mykeyspace.users WHERE id=42"`
- `nodetool tpstats | grep -E 'ReadRepair|Read'`

**Examples:**
- cqlsh -e "CONSISTENCY QUORUM; SELECT * FROM mykeyspace.users WHERE id=42"
- cqlsh -e "TRACING ON; SELECT * FROM mykeyspace.users WHERE id=42"
- cqlsh -e "CONSISTENCY EACH_QUORUM; SELECT COUNT(*) FROM mykeyspace.users"
