---
trigger: glob
description: "Builds robust ETL pipelines: extraction, transformation, loading, with validation and scheduling."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.sql"]
---

# Etl Pipeline

Builds robust ETL pipelines: extraction, transformation, loading, with validation and scheduling.

## Instructions

# ETL Pipeline

Designs and implements extract-transform-load pipelines that are idempotent,
validated, and monitored.

## When to Use

- Moving data from sources into a warehouse
- Building repeatable, dated batch jobs
- Adding validation and observability to existing flows

## Real Commands

```bash
# Run the pipeline for a date
python -m etl_pkg run --env prod --date 2024-01-15 --incremental

# Spark-based transforms
spark-submit --master yarn --deploy-mode cluster jobs/extract.py --input s3://raw/events/ --output s3://curated/events/

# Lightweight transform with jq
jq '.items[] | select(.status == "ok") | {id, value}' raw.json > clean.json

# Load into Postgres
psql -d warehouse -c "\copy staging.events FROM 'clean.csv' CSV HEADER"

# Validate
python -m pytest tests/ -q
python -m etl_pkg validate --env prod --date 2024-01-15
```

## Pipeline Contract

1. Extract writes raw data untouched to a landing zone
2. Transform is pure SQL/DataFrame logic, versioned
3. Load uses upsert or partitioned overwrite (idempotent)
4. Validate row counts and nulls before promoting
5. Log metrics: rows in, rows out, duration

## Best Practices

- Partition by date; delete+reload for reprocessing
- Test with fixtures, not production data
- Make every step idempotent so backfills are safe
- Alert on row-count anomalies
- Keep credentials out of code (env vars / secret manager)

## Example Response

Runs the pipeline, reports rows extracted/transformed/loaded, validation results,
and duration; if a step fails, isolates the step and error from logs.

## Capabilities

### etl-pipeline
Implement and run ETL jobs with Python, Spark, and CLI tools

**Commands:**
- `python -m etl_pkg run --env prod --date 2024-01-15`
- `spark-submit --master yarn --deploy-mode cluster jobs/extract.py --input s3://raw/ --output s3://curated/`
- `jq '.items[] | {id: .id, value: .value}' raw.json > clean.json`
- `psql -d warehouse -c "\\copy staging.events FROM 'clean.csv' CSV HEADER"`
- `python -m pytest tests/ -q`

**Examples:**
- python -m etl_pkg run --env staging --date 2024-01-15 --incremental
- spark-submit --master local[4] jobs/transform.py
- airflow dags trigger etl_pipeline --conf '{"date": "2024-01-15"}'
