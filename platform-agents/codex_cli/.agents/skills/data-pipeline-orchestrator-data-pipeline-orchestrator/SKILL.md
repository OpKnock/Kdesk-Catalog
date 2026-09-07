---
name: "data-pipeline-orchestrator-data-pipeline-orchestrator"
description: "Orchestrates data pipelines with Dagster, Prefect, and Airflow: job definitions, schedules, and runs. Use when working with dagster orchestration or when the user mentions dagster orchestration."
license: "MIT"
compatibility: "Requires airflow, dagster, prefect, python, great-expectations, dbt."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "data"}
allowed-tools: "Glob Grep Read Bash(dagster:*)"
---

Orchestrates data pipelines with Dagster, Prefect, and Airflow: job definitions, schedules, and runs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `dagster dev`
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

**Parameters:**
- `module` (string): Python module with definitions (-m)
- `select` (string): Asset selection, e.g. asset_name+ or tag:daily
- `config` (string): Run config YAML file

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

## References
- [Dagster docs](https://docs.dagster.io/)
- [Prefect docs](https://docs.prefect.io/)
- [Airflow orchestration docs](https://airflow.apache.org/docs/apache-airflow/stable/)
