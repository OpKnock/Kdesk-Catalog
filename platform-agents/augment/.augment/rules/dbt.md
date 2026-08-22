---
type: agent_requested
description: "Develops and runs dbt models and tests: data transformation, testing, and documentation generation."
---

# Dbt

Develops and runs dbt models and tests: data transformation, testing, and documentation generation.

## Instructions

# dbt

Analytics engineering: transforms raw tables into modeled datasets with SQL,
enforces tests, and generates docs.

## When to Use

- Building a staging-to-marts transformation layer
- Testing data quality (nulls, uniqueness, referential integrity)
- Documenting lineage and generating docs site

## Real Commands

```bash
# Verify connection
sudo dbt debug

# Compile-only (no run)
sudo dbt compile --select stg_orders

# Run everything
sudo dbt run

# Run a model and its downstream
sudo dbt run --select stg_orders+ --target prod

# Tests
sudo dbt test
sudo dbt test --select source:raw.orders --store-failures

# Build = run + test in one
sudo dbt build --select my_model+

# Docs
sudo dbt docs generate
sudo dbt docs serve --port 8080
```

## Example Model (models/marts/fct_orders.sql)

```sql
select
  o.order_id,
  c.customer_id,
  o.order_date,
  sum(o.amount) as amount
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c using (customer_id)
group by 1, 2, 3
```

## Example Test (schema.yml)

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests: [unique, not_null]
```

## Best Practices

- One model per file, named after the relation
- Use `ref()` and `source()`, never hardcoded table names
- Keep models modular: staging -> intermediate -> marts
- Test every primary key for unique/not_null
- Run `dbt build` in CI, not just `dbt run`

## Example Response

For a failing test: reports the model/column, the test type, and the number of
failing rows, then proposes the data fix or test adjustment.

## Capabilities

### dbt-core
Run models, tests, and docs for dbt projects

**Commands:**
- `dbt debug`
- `dbt run`
- `dbt test`
- `dbt build --select my_model+`
- `dbt docs generate && dbt docs serve --port 8080`

**Examples:**
- dbt run --select tag:daily
- dbt test --select source:raw.orders --store-failures
- dbt compile --select stg_orders