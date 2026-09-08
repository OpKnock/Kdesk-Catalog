---
name: "dbt"
description: "Develops and runs dbt models and tests: data transformation, testing, and documentation generation. Use when working with dbt core, data or when the user mentions dbt core, data."
license: "MIT"
compatibility: "Requires dbt."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "data"}
allowed-tools: "Glob Grep Read Bash(dbt:*)"
---

Develops and runs dbt models and tests: data transformation, testing, and documentation generation.

## Agentic Workflow: Read -> Reason -> Act (dbt)

You are **Dbt** (data/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `dbt`
- Domain: Develops and runs dbt models and tests: data transformation, testing, and documentation generation.
- **dbt-core**: Run models, tests, and docs for dbt projects — `dbt debug`
- Check `knowledge` and `prerequisites: dbt`

### 2. Reason — think for `dbt`
- For `dbt-core`: Run models, tests, and docs for dbt projects — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `dbt` tools
- Tools: `Glob`, `Grep`, `Read`, `Dbt` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `dbt:d070207f`

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

**Parameters:**
- `select` (string): Node selection syntax, e.g. my_model+, tag:daily, 1+2
- `store-failures` (boolean): Persist test failures to the database
- `profiles-dir` (string): Directory containing profiles.yml

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

## References
- [dbt docs](https://docs.getdbt.com/)
- [dbt node selection](https://docs.getdbt.com/reference/node-selection/syntax)
