---
name: "performance-tuning"
description: "Tunes database performance: EXPLAIN plans, slow query logs, buffer/cache settings, and load testing."
type: knowledge
triggers: ["performance-tuning", "query-tuning"]
---

# Performance Tuning

Tunes database performance: EXPLAIN plans, slow query logs, buffer/cache settings, and load testing.

## Instructions

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
