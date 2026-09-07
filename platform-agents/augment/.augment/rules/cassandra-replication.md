---
type: agent_requested
description: "Manages Cassandra replication: replication factors, keyspace strategies, endpoint mapping, and consistency levels. Use when working with keyspace replication, endpoints, consistency, api or when the user mentions keyspace replication, endpoints, consistency, api."
---

Manages Cassandra replication: replication factors, keyspace strategies, endpoint mapping, and consistency levels.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cqlsh -e "DESCRIBE KEYSPACE mykeyspace"`, `nodetool getendpoints mykeyspace users 42`
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