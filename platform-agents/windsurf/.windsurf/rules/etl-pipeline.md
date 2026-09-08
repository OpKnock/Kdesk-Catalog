---
trigger: glob
description: "Builds robust ETL pipelines: extraction, transformation, loading, with validation and scheduling. Use when working with etl pipeline, data or when the user mentions etl pipeline, data."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.sql"]
---

Builds robust ETL pipelines: extraction, transformation, loading, with validation and scheduling.

## Agentic Workflow: Read -> Reason -> Act (etl-pipeline)

You are **Etl Pipeline** (data/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `etl-pipeline`
- Domain: Builds robust ETL pipelines: extraction, transformation, loading, with validation and scheduling.
- **etl-pipeline**: Implement and run ETL jobs with Python, Spark, and CLI tools — `python -m etl_pkg run --env prod --date 2024-01-15`
- Check `knowledge` and `prerequisites: psql, python, spark-submit`

### 2. Reason — think for `etl-pipeline`
- For `etl-pipeline`: Implement and run ETL jobs with Python, Spark, and CLI tools — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `etl-pipeline` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Spark-submit` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `etl-pipeline:8c9521ae`

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

**Parameters:**
- `env` (string): Environment: dev, staging, prod
- `date` (string): Logical execution date for the pipeline
- `incremental` (boolean): Process only the delta since the last run

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

## References
- [Apache Spark SQL guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Airflow ETL best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
