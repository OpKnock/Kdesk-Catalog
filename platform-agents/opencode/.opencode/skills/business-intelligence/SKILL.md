---
name: "business-intelligence"
description: "Builds BI pipelines with SQL warehouses, dbt, Metabase, and Superset: metrics modeling, dashboards, and scheduled reporting."
---

# business-intelligence

Builds BI pipelines with SQL warehouses, dbt, Metabase, and Superset: metrics modeling, dashboards, and scheduled reporting.

## Instructions

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
