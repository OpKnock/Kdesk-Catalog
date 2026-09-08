---
name: "flink-sql"
description: "Stream processing with Flink SQL: start the SQL client, run streaming queries against Kafka topics, and manage table sources and sinks. Use when working with flink sql client, api or when the user mentions flink sql client, api."
type: knowledge
triggers: ["flink-sql", "flink-sql-client"]
---

Stream processing with Flink SQL: start the SQL client, run streaming queries against Kafka topics, and manage table sources and sinks.

## Agentic Workflow: Read -> Reason -> Act (flink-sql)

You are **Flink Sql** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `flink-sql`
- Domain: Stream processing with Flink SQL: start the SQL client, run streaming queries against Kafka topics, and manage table sources and sinks.
- **flink-sql-client**: Run Flink SQL queries, define sources/sinks, and manage jobs. — `sql-client.sh embedded --defaults conf/sql-client-defaults.yaml`
- Check `knowledge` and `prerequisites: flink, kafka-console-producer, sql-client.sh`

### 2. Reason — think for `flink-sql`
- For `flink-sql-client`: Run Flink SQL queries, define sources/sinks, and manage jobs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `flink-sql` tools
- Tools: `Glob`, `Grep`, `Read`, `Sql-client.sh`, `Kafka-console-producer` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `flink-sql:5056a19a`

# Flink SQL

## What this skill does

Flink SQL turns stream processing into SQL: you declare Kafka topics as tables and run continuous queries over them. The sql-client executes interactively or from .sql scripts.

## When to use

- Aggregating event streams (counts, sums, windows)
- Joining streaming data with static dimension data
- Prototyping pipelines before writing Java/Scala jobs

## Real commands

```bash
# Interactive SQL client
sql-client.sh embedded --defaults conf/sql-client-defaults.yaml

# Execute a script headless
sql-client.sh embedded -f /opt/jobs/orders.sql

# Seed a Kafka topic to test against
kafka-console-producer --bootstrap-server localhost:9092 --topic orders.events
```

## SQL example

```sql
CREATE TABLE orders (
  order_id STRING,
  amount DECIMAL(10, 2),
  ts TIMESTAMP(3),
  WATERMARK FOR ts AS ts - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'orders.events',
  'properties.bootstrap.servers' = 'localhost:9092',
  'format' = 'json',
  'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE hourly_sales (
  window_start TIMESTAMP(3),
  total_amount DECIMAL(14, 2)
) WITH (
  'connector' = 'print'
);

INSERT INTO hourly_sales
SELECT TUMBLE_START(ts, INTERVAL '1' HOUR), SUM(amount)
FROM orders
GROUP BY TUMBLE(ts, INTERVAL '1' HOUR);
```

## Testing

```bash
# Run a bounded test: read from a file sink with print connector
sql-client.sh embedded -f /opt/jobs/test.sql
```

## Best practices

- Always define WATERMARKs for event-time aggregations.
- Set checkpointing (default 60s) for exactly-once state.
- Prefer `scan.startup.mode = 'earliest-offset'` for reprocessing.
- Keep DDL in .sql scripts versioned with the job.
- Test with the print connector before wiring real sinks.

## Capabilities

### flink-sql-client
Run Flink SQL queries, define sources/sinks, and manage jobs.

**Parameters:**
- `script-file` (string): Path to a .sql script for batch execution
- `kafka-topic` (string): Topic backing the source/sink table
- `checkpoint-interval` (string): Checkpoint interval like 60s

**Commands:**
- `sql-client.sh embedded --defaults conf/sql-client-defaults.yaml`
- `sql-client.sh embedded -f /opt/jobs/orders.sql`
- `kafka-console-producer --bootstrap-server localhost:9092 --topic orders.events`
- `sql-client.sh embedded --help`
- `flink run -d -c org.example.StreamJob /opt/jobs/job.jar`

**Examples:**
- sql-client.sh embedded -f /opt/jobs/orders.sql
- kafka-console-producer --bootstrap-server localhost:9092 --topic orders.events
- sql-client.sh embedded --help

## References
- [Flink SQL Reference](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/overview/)
- [Flink SQL Client](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sqlclient/)
