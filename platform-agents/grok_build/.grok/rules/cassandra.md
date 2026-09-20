Operates Cassandra: cqlsh queries, schema management, and node health via nodetool.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cqlsh -e "DESCRIBE KEYSPACES;"`
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

# Cassandra

Distributed NoSQL operations: CQL queries, schema changes, and cluster health
with nodetool.

## When to Use

- Querying or writing data via cqlsh
- Running repairs and checking node state
- Applying schema changes to a cluster

## Real Commands

```bash
# Connect and explore
sudo cqlsh
sudo cqlsh -e "DESCRIBE KEYSPACES;"

# Queries
sudo cqlsh -k app -e "SELECT * FROM orders WHERE order_id = 'abc-123';"
sudo cqlsh -e "SELECT * FROM app.orders LIMIT 10;"

# Schema script
sudo cqlsh -f schema.cql

# Node health
sudo nodetool status
sudo nodetool status app

# Repairs (primary range)
sudo nodetool repair -pr app

# Activity
sudo nodetool tpstats
sudo nodetool compactionstats
sudo nodetool tablestats app.orders
```

## Schema Example (schema.cql)

```sql
CREATE KEYSPACE IF NOT EXISTS app WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': 3};
CREATE TABLE IF NOT EXISTS app.orders (
  order_id uuid PRIMARY KEY,
  customer_id uuid,
  amount decimal,
  created_at timestamp
);
```

## Best Practices

- Always qualify queries with the partition key
- Run repairs during low traffic with `-pr`
- Never `DESCRIBE`-drift: apply schema via versioned CQL files
- Check `tpstats` for drop and latency issues
- Watch `nodetool status` for UN (up-normal) on all nodes

## Example Response

For a slow cluster: reports nodetool status, compaction stats, and tpstats; then
recommends repairs, compactions, or query fixes.

## Capabilities

### cassandra-cli
Query and manage Cassandra with cqlsh and nodetool

**Parameters:**
- `keyspace` (string): Keyspace to use (-k)
- `file` (string): CQL script file to execute (-f)
- `parallel` (boolean): Run repair in parallel (-pr)

**Commands:**
- `cqlsh -e "DESCRIBE KEYSPACES;"`
- `cqlsh -e "SELECT * FROM app.orders LIMIT 10;"`
- `cqlsh -f schema.cql`
- `nodetool status`
- `nodetool repair -pr`

**Examples:**
- cqlsh -k app -e "SELECT count(*) FROM orders;"
- nodetool tpstats | head -20
- nodetool compactionstats

## References
- [Cassandra docs](https://cassandra.apache.org/doc/latest/)
- [nodetool reference](https://cassandra.apache.org/doc/latest/cassandra/operating/)