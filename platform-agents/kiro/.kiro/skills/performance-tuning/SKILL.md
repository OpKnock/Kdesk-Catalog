---
name: "performance-tuning"
description: "Tunes database performance: EXPLAIN plans, slow query logs, buffer/cache settings, and load testing. Use when working with query tuning, database or when the user mentions query tuning, database."
license: "MIT"
compatibility: "Requires mysql, mysqldumpslow, psql."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "database"}
allowed-tools: "Glob Grep Read Bash(mysql:*) Bash(mysqldumpslow:*) Bash(psql:*)"
---

Tunes database performance: EXPLAIN plans, slow query logs, buffer/cache settings, and load testing.

## Agentic Workflow: Read -> Reason -> Act (performance-tuning)

You are **Performance Tuning** (database/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — database context for `performance-tuning`
- Domain: Tunes database performance: EXPLAIN plans, slow query logs, buffer/cache settings, and load testing.
- **query-tuning**: Analyze query plans and find slow queries across engines — `psql -d app -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE created_at`
- Check `knowledge` and `prerequisites: mysql, mysqldumpslow, psql`

### 2. Reason — think for `performance-tuning`
- For `query-tuning`: Analyze query plans and find slow queries across engines — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `performance-tuning` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Mysql` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `performance-tuning:4082c52e`

# Performance Tuning

Diagnoses slow databases: plan analysis, slow-query capture, configuration
changes, and verification with load tests.

## When to Use

- A specific query is slow
- General database sluggishness
- Before/after verification of config changes

## Real Commands

```bash
# PostgreSQL: real execution plan
psql -d app -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE created_at > now() - interval '1 day';"

# Top slow statements
psql -d app -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# MySQL: enable slow log
mysql -u root -p -e "SET GLOBAL slow_query_log=ON; SET GLOBAL long_query_time=2;"

# MySQL: plan
mysql -u root -p appdb -e "EXPLAIN SELECT * FROM orders WHERE status='paid';"

# Summarize slow logs
sudo mysqldumpslow -s t /var/log/mysql/slow.log | head -20

# Load test after tuning
sudo pgbench -c 10 -j 2 -T 60 app
```

## Tuning Checklist

1. Capture the slow query (slow log / pg_stat_statements)
2. EXPLAIN it: look for seq scans, high estimated vs actual rows
3. Add/adjust indexes; rewrite if needed
4. Check cache hit ratio (pg_stat_bgwriter / InnoDB buffer pool)
5. Re-test with pgbench or equivalent

## Best Practices

- Tune one variable at a time and measure
- Index on WHERE/ORDER/JOIN columns, not everything
- Watch for hidden full table scans
- Verify plans changed after ANALYZE / statistics update
- In prod, run EXPLAIN (ANALYZE) on a copy first

## Example Response

Shows the before/after EXPLAIN output, the index added, and pgbench results
demonstrating the improvement.

## Capabilities

### query-tuning
Analyze query plans and find slow queries across engines

**Parameters:**
- `analyze` (boolean): Execute the query and show real timings/buffers
- `buffers` (boolean): Include buffer hit/miss stats in the plan
- `sort` (string): Sort key for mysqldumpslow: t (time), c (count), l (lock)

**Commands:**
- `psql -d app -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE created_at > now() - interval '1 day';"`
- `mysql -u root -p -e "SET GLOBAL slow_query_log=ON; SET GLOBAL long_query_time=2;"`
- `mysql -u root -p appdb -e "EXPLAIN SELECT * FROM orders WHERE status='paid';"`
- `psql -d app -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"`
- `mysqldumpslow -s t /var/log/mysql/slow.log | head -20`

**Examples:**
- psql -d app -c "\d+ orders"
- mysql -u root -p appdb -e "SHOW INDEX FROM orders;"
- pt-query-digest /var/log/mysql/slow.log | head -80

## References
- [PostgreSQL EXPLAIN guide](https://www.postgresql.org/docs/current/using-explain.html)
- [MySQL slow query log](https://dev.mysql.com/doc/refman/8.0/en/slow-query-log.html)
- [pg_stat_statements docs](https://www.postgresql.org/docs/current/pgstatstatements.html)
