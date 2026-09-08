---
name: "business-intelligence"
description: "Builds BI pipelines with SQL warehouses, dbt, Metabase, and Superset: metrics modeling, dashboards, and scheduled reporting. Use when working with bi warehouses, bi modeling or when the user mentions bi warehouses, bi modeling."
type: knowledge
triggers: ["business-intelligence", "bi-warehouses", "bi-modeling"]
---

Builds BI pipelines with SQL warehouses, dbt, Metabase, and Superset: metrics modeling, dashboards, and scheduled reporting.

## Agentic Workflow: Read -> Reason -> Act (business-intelligence)

You are **business-intelligence** (data) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `business-intelligence`
- Domain: Builds BI pipelines with SQL warehouses, dbt, Metabase, and Superset: metrics modeling, dashboards, and scheduled reporting.
- **bi-warehouses**: Query and manage warehouse data. — `psql "postgres://user:pass@localhost/analytics" -c "SELECT count(*) FROM orders"`
- **bi-modeling**: Model metrics with dbt. — `dbt init my_project`
- Check `knowledge` and `prerequisites: snowflake, bigquery, dbt, airflow`

### 2. Reason — think for `business-intelligence`
- For `bi-warehouses`: Query and manage warehouse data. — decide which checks to run
- For `bi-modeling`: Model metrics with dbt. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `business-intelligence` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Duckdb` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `business-intelligence:28860413`

# Business Intelligence

Build analytics pipelines and dashboards.

## When to Use

- Reporting revenue, retention, and funnel metrics
- Self-serve dashboards for stakeholders
- Metrics engineering with dbt
- One-off analysis with DuckDB/psql

## Commands

```bash
# Ad-hoc querying
psql analytics -c "SELECT count(*) FROM orders"
duckdb analytics.db "SELECT * FROM orders LIMIT 10"
duckdb -csv analytics.db "SELECT date_trunc('day', created_at) d, count(*) FROM orders GROUP BY 1"

# dbt modeling
dbt init my_project
dbt run
dbt test
dbt build
dbt docs generate
dbt docs serve

# Metabase
java -jar metabase.jar
```

## dbt Model

```sql
-- models/marts/daily_orders.sql
SELECT
  date_trunc('day', created_at) AS day,
  count(*) AS orders,
  sum(total) AS revenue
FROM {{ ref('stg_orders') }}
GROUP BY 1
```

## Best Practices

- Define metrics once in dbt, reuse everywhere
- Write tests for uniqueness, not-null, and freshness
- Use semantic layers so dashboard numbers agree
- Document models with dbt docs generate
- Schedule dbt build, then refresh dashboards
- Keep raw data immutable; model in layers (staging, marts)

## Capabilities

### bi-warehouses
Query and manage warehouse data.

**Parameters:**
- `connection` (string): Connection string
- `sql` (string): Query text

**Commands:**
- `psql "postgres://user:pass@localhost/analytics" -c "SELECT count(*) FROM orders"`
- `duckdb analytics.db "SELECT count(*) FROM orders"`
- `mysql -u root -p analytics -e "SHOW TABLES"`
- `duckdb -csv analytics.db "SELECT * FROM orders LIMIT 10"`

**Examples:**
- psql analytics -c "\\dt"
- duckdb analytics.db "SELECT date_trunc('day', created_at) d, count(*) FROM orders GROUP BY 1"
- python -m venv .venv

### bi-modeling
Model metrics with dbt.

**Parameters:**
- `select` (string): Model selection
- `test` (boolean): Run dbt data tests

**Commands:**
- `dbt init my_project`
- `dbt run`
- `dbt test`
- `dbt build`
- `dbt docs generate`

**Examples:**
- dbt run --select stg_orders
- dbt test --select tag:core
- dbt docs serve

## References
- [dbt Docs](https://docs.getdbt.com)
- [DuckDB Docs](https://duckdb.org/docs/)
- [Metabase Docs](https://www.metabase.com/docs/latest/)
