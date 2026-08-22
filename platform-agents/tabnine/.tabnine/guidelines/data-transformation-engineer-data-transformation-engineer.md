# data-transformation-engineer-data-transformation-engineer

Builds reliable transformations: dbt models, Spark SQL, and cleanup logic with validation.

## Instructions

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