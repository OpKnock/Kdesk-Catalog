---
name: "data-pipeline-orchestrator-data-pipeline-orchestrator"
description: "Orchestrates data pipelines with Dagster, Prefect, and Airflow: job definitions, schedules, and runs."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# data-pipeline-orchestrator-data-pipeline-orchestrator

Orchestrates data pipelines with Dagster, Prefect, and Airflow: job definitions, schedules, and runs.

## Instructions

# Data Pipeline Orchestrator

Designs and runs orchestrated pipelines: dependency-aware jobs, scheduling,
backfills, and failure handling.

## When to Use

- Scheduling multi-step data jobs with dependencies
- Backfilling historical ranges
- Debugging failed runs and retries

## Real Commands

```bash
# Dagster: run the dev UI with code location
sudo dagster dev

# Materialize assets
sudo dagster materialize -m assets.py --select 'orders+' -p daily

# Execute a job with config
sudo dagster job execute -j etl_job --config run.yaml

# Inspect runs
sudo dagster run list --status failed

# Prefect
prefect deployment run etl_flow/prod -p '{"date": "2024-01-15"}'
prefect flow-run ls --limit 10

# Airflow
airflow dags backfill -s 2024-01-01 -e 2024-01-07 daily_etl
airflow dags list-runs -d daily_etl
```

## Dependency Design

```python
# assets.py
from dagster import asset

@asset
def raw_events(): ...

@asset(deps=[raw_events])
def cleaned_events(): ...
```

## Best Practices

- Model dependencies explicitly; orchestrators enforce them
- Make runs idempotent so retries and backfills are safe
- Use configs (dates, env) not hardcoded values
- Alert on failure with retry policies
- Keep pipeline code testable outside the orchestrator

## Example Response

For a failed run: identifies the failing step and error, applies the fix, and
re-runs the step or backfills the failed window.

## Capabilities

### dagster-orchestration
Develop and run Dagster assets and jobs

**Commands:**
- `dagster dev`
- `dagster asset list`
- `dagster job execute -j my_job`
- `dagster materialize -m assets.py`
- `dagster schedule list`

**Examples:**
- dagster materialize -m assets.py --select 'orders_asset+'
- dagster job execute -j etl_job --config run.yaml
- dagster run list --status success