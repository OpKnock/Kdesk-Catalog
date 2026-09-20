---
name: "snowflake"
description: "Works with Snowflake: SQL execution via snowsql, warehouses, stages, and query performance."
type: knowledge
triggers: ["snowflake", "snowsql"]
---

# Snowflake

Works with Snowflake: SQL execution via snowsql, warehouses, stages, and query performance.

## Instructions

# Snowflake

Data warehouse operations with snowsql: SQL execution, loading via stages,
warehouse management, and query diagnostics.

## When to Use

- Running ad-hoc and scripted SQL
- Loading files from stages into tables
- Investigating slow queries and warehouse usage

## Real Commands

```bash
# Connect and run one query
snowsql -a myorg-account -u jdoe -d analytics -s core -w etl_wh \
  -q "SELECT CURRENT_WAREHOUSE(), CURRENT_ROLE();"

# Run a script file
snowsql -a myorg-account -u jdoe -f scripts/schema.sql --warehouse=etl_wh \
  -o exit_on_error=true -o echo=true

# Load data from a stage
snowsql -q "COPY INTO raw.events FROM @my_stage/events FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1);"

# Warehouse state
snowsql -q "SHOW WAREHOUSES;" -o output_format=json

# Slow query analysis
snowsql -q "SELECT query_id, total_elapsed_time/1000 AS secs, query_text FROM table(information_schema.query_history(result_limit=>10)) ORDER BY total_elapsed_time DESC;"
```

## Best Practices

- Set `-o exit_on_error=true` in migrations to stop on failures
- Use roles, not individual credentials, for automation
- Suspend warehouses in dev (auto_suspend) to control cost
- Load via stages + COPY INTO rather than insert-by-insert
- Check `QUERY_HISTORY` for cost and performance diagnosis

## Example Response

For a slow pipeline: finds the slow queries in query_history, checks warehouse
size and cache misses, and recommends sizing or clustering changes.

## Capabilities

### snowsql
Execute SQL, scripts, and configuration against Snowflake

**Commands:**
- `snowsql -a myorg-account -u jdoe -d analytics -s core`
- `snowsql -q "SELECT CURRENT_WAREHOUSE(), CURRENT_ROLE();"`
- `snowsql -f scripts/schema.sql --warehouse=etl_wh`
- `snowsql -o exit_on_error=true -f migrations/001.sql`
- `snowsql -q "SHOW WAREHOUSES;" -o output_format=json`

**Examples:**
- snowsql -a myorg-account -u jdoe -d analytics -s core -w compute_wh
- snowsql -q "COPY INTO raw.events FROM @stage/events FILE_FORMAT=(TYPE=CSV)"
- snowsql -q "SELECT query_id, total_elapsed_time/1000 secs FROM table(information_schema.query_history()) ORDER BY total_elapsed_time DESC LIMIT 10;"
