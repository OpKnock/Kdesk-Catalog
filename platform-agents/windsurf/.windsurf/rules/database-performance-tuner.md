---
trigger: glob
description: "Deep database performance work: plan analysis, slow-log mining, buffer tuning, and load verification. Use when working with deep tuning or when the user mentions deep tuning."
globs: ["**/*.r", "**/*.sh", "**/*.sql"]
---

Deep database performance work: plan analysis, slow-log mining, buffer tuning, and load verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `psql -d app -c "EXPLAIN (ANALYZE, BUFFERS, TIMING) SELECT ..`
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

# Database Performance Tuner

End-to-end performance engineering for databases: find the pain, tune the plan
or config, measure the improvement.

## When to Use

- Response-time regressions
- Capacity planning with load tests
- Post-migration performance validation

## Real Commands

```bash
# PostgreSQL: worst tables by seq scan
psql -d app -c "SELECT relname, seq_scan, idx_scan FROM pg_stat_user_tables ORDER BY seq_scan DESC LIMIT 10;"

# Real plan
psql -d app -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE created_at > now() - interval '7 days';"

# Top statements
psql -d app -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"

# MySQL slow log analysis
sudo mysqldumpslow -s t /var/log/mysql/mysql-slow.log | head -40
sudo pt-query-digest /var/log/mysql/mysql-slow.log --limit 10

# Current settings
mysql -e "SHOW VARIABLES LIKE 'innodb_buffer_pool_size';"

# Load test
sudo pgbench -c 20 -j 4 -T 120 -S app
```

## Methodology

1. Measure: capture the slow queries with timings
2. Isolate: EXPLAIN ANALYZE the worst offenders
3. Fix: index, rewrite, or config change (one at a time)
4. Verify: re-run the plan and a load test
5. Document: record the delta for the change review

## Common Wins

- Missing index on WHERE/JOIN columns
- seq scan where index scan expected
- Low cache hit ratio (shared_buffers / buffer pool too small)
- Lock contention on hot rows

## Example Response

Ranks slow statements, applies the index/plan fix, and shows before/after
timings plus pgbench percentiles proving the gain.

## Capabilities

### deep-tuning
Analyze query plans, slow logs, and configuration for peak performance

**Parameters:**
- `analyze` (boolean): Execute queries in EXPLAIN to get real timings
- `sort` (string): mysqldumpslow sort key: t, at, c, l
- `limit` (integer): Limit for report rows

**Commands:**
- `psql -d app -c "EXPLAIN (ANALYZE, BUFFERS, TIMING) SELECT ..."`
- `mysqldumpslow -s t /var/log/mysql/mysql-slow.log | head -40`
- `pt-query-digest /var/log/mysql/mysql-slow.log --limit 10`
- `psql -d app -c "SELECT relname, seq_scan, idx_scan FROM pg_stat_user_tables ORDER BY seq_scan DESC LIMIT 10;"`
- `pgbench -c 20 -j 4 -T 120 -S app`

**Examples:**
- mysql -e "SHOW ENGINE INNODB STATUS\G" | head -60
- psql -d app -c "SHOW shared_buffers; SHOW work_mem; SHOW effective_cache_size;"
- pg_stat_statements: psql -d app -c "SELECT query, mean_exec_time, calls FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"

## References
- [PostgreSQL performance docs](https://www.postgresql.org/docs/current/performance-tips.html)
- [Percona Toolkit docs](https://www.percona.com/software/database-tools/percona-toolkit)
- [MySQL InnoDB tuning](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html)
