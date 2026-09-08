---
trigger: glob
description: "Manages Cassandra replication: replication factors, keyspace strategies, endpoint mapping, and consistency levels. Use when working with keyspace replication, endpoints, consistency, api or when the user mentions keyspace replication, endpoints, consistency, api."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

Manages Cassandra replication: replication factors, keyspace strategies, endpoint mapping, and consistency levels.

## Agentic Workflow: Read -> Reason -> Act (cassandra-replication)

You are **Cassandra Replication** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `cassandra-replication`
- Domain: Manages Cassandra replication: replication factors, keyspace strategies, endpoint mapping, and consistency levels.
- **keyspace-replication**: Set and inspect replication configuration. — `cqlsh -e "DESCRIBE KEYSPACE mykeyspace"`
- **endpoints**: Map partition keys to replicas. — `nodetool getendpoints mykeyspace users 42`
- **consistency**: Set and test consistency levels. — `cqlsh -e "CONSISTENCY QUORUM"`
- Check `knowledge` and `prerequisites: cqlsh, nodetool`

### 2. Reason — think for `cassandra-replication`
- For `keyspace-replication`: Set and inspect replication configuration. — decide which checks to run
- For `endpoints`: Map partition keys to replicas. — decide which checks to run
- For `consistency`: Set and test consistency levels. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cassandra-replication` tools
- Tools: `Glob`, `Grep`, `Read`, `Cqlsh`, `Nodetool` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cassandra-replication:b9041e6b`

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

**Parameters:**
- `keyspace` (string): Keyspace name
- `dc_replication` (string): Per-DC RF map
- `strategy` (string): NetworkTopologyStrategy or SimpleStrategy

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

**Parameters:**
- `keyspace` (string): Keyspace
- `table` (string): Table
- `partition_key` (string): Partition key value

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

**Parameters:**
- `consistency` (string): Consistency level
- `trace` (boolean): Enable tracing

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

## References
- [Cassandra Dynamo Architecture](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)
- [Cassandra Consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/guarantees.html)
- [nodetool getendpoints](https://cassandra.apache.org/doc/latest/cassandra/operating/nodetool/)
