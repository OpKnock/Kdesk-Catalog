---
name: "data-transformation-engineer-data-transformation-engineer"
description: "Builds reliable transformations: dbt models, Spark SQL, and cleanup logic with validation. Use when working with transforms or when the user mentions transforms."
type: knowledge
triggers: ["data-transformation-engineer-data-transformation-engineer", "transforms"]
---

Builds reliable transformations: dbt models, Spark SQL, and cleanup logic with validation.

## Agentic Workflow: Read -> Reason -> Act (data-transformation-engineer-data-transformation-engineer)

You are **data-transformation-engineer-data-transformation-engineer** (data) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `data-transformation-engineer-data-transformation-engineer`
- Domain: Builds reliable transformations: dbt models, Spark SQL, and cleanup logic with validation.
- **transforms**: Create and run SQL/Python transformations with lineage and tests — `dbt run --select stg_orders+`
- Check `knowledge` and `prerequisites: node.js, python, jsonschema, ajv`

### 2. Reason — think for `data-transformation-engineer-data-transformation-engineer`
- For `transforms`: Create and run SQL/Python transformations with lineage and tests — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `data-transformation-engineer-data-transformation-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Dbt`, `Spark-sql` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `data-transformation-engineer-data-transformation-engineer:f4f8f47d`

# Data Transformation Engineer

Turns raw data into analysis-ready tables with documented, tested transformations.

## When to Use

- Building staging/cleaning/mart layers
- Aggregating raw events into metrics tables
- Enforcing tests on transformation output

## Real Commands

```bash
# dbt run with lineage
sudo dbt run --select stg_orders+

# Test marts
sudo dbt test --select models/marts --store-failures

# Spark SQL ad-hoc
spark-sql -e "SELECT date, sum(amount) AS revenue FROM parquet.`s3://curated/orders/` GROUP BY 1 ORDER BY 1;"

# JSONL cleanup with jq
jq -c 'select(.status=="paid") | {id, amount, ts}' raw_orders.json > paid.jsonl

# Full pipeline test in dev then prod
sudo dbt build --select tag:marts --target dev
sudo dbt build --select tag:marts --target prod
```

## Transform Pattern

```sql
-- stg_orders.sql
select
  order_id,
  customer_id,
  cast(order_date as date) as order_date,
  amount
from {{ source('raw', 'orders') }}
where amount is not null
```

## Best Practices

- One transform = one purpose; keep models narrow
- Test primary keys and distribution (nulls, negatives)
- Materialize as views in staging, tables in marts
- Document business meaning next to the model
- Reproduce transformations deterministically for reruns

## Example Response

Runs the selected transforms, reports rows affected per model, test outcomes,
and flags data-quality issues with sample rows.

## Capabilities

### transforms
Create and run SQL/Python transformations with lineage and tests

**Parameters:**
- `select` (string): Node or tag selection for run/test
- `target` (string): dbt environment target (dev/prod)
- `input` (string): Input location for Spark jobs

**Commands:**
- `dbt run --select stg_orders+`
- `dbt test --select models/marts`
- `spark-sql -e "SELECT date, sum(amount) FROM parquet.`s3://curated/orders/` GROUP BY 1;"`
- `jq -c 'select(.status=="paid") | {id, amount}' raw_orders.json > paid.jsonl`
- `dbt docs generate && dbt docs serve`

**Examples:**
- dbt run --select tag:marts --target prod
- spark-submit --master local[4] jobs/transform.py --input s3://raw --output s3://curated
- jq -s 'group_by(.customer) | map({customer: .[0].customer, total: map(.amount)|add})' orders.jsonl

## References
- [dbt model docs](https://docs.getdbt.com/docs/build/models)
- [Spark SQL reference](https://spark.apache.org/docs/latest/sql-ref.html)
