---
name: "business-intelligence"
description: "Builds BI pipelines with SQL warehouses, dbt, Metabase, and Superset: metrics modeling, dashboards, and scheduled reporting. Use when working with bi warehouses, bi modeling or when the user mentions bi warehouses, bi modeling."
license: "MIT"
compatibility: "Requires snowflake, bigquery, dbt, airflow, metabase."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "data"}
allowed-tools: "Glob Grep Read Bash(dbt:*) Bash(duckdb:*) Bash(mysql:*) Bash(psql:*)"
---

Builds BI pipelines with SQL warehouses, dbt, Metabase, and Superset: metrics modeling, dashboards, and scheduled reporting.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `psql "postgres://user:pass@localhost/analytics" -c "SELECT c`, `dbt init my_project`
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
