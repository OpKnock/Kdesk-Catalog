---
name: "airflow"
description: "Builds and operates Airflow DAGs: local setup, DAG testing, task runs, and backfills. Use when working with airflow operations, data or when the user mentions airflow operations, data."
---

Builds and operates Airflow DAGs: local setup, DAG testing, task runs, and backfills.

## Agentic Workflow: Read -> Reason -> Act (airflow)

You are **Airflow** (data/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `airflow`
- Domain: Builds and operates Airflow DAGs: local setup, DAG testing, task runs, and backfills.
- **airflow-operations**: Manage Airflow metadata, users, DAGs, and task runs from the CLI — `airflow db init`
- Check `knowledge` and `prerequisites: airflow`

### 2. Reason — think for `airflow`
- For `airflow-operations`: Manage Airflow metadata, users, DAGs, and task runs from the CLI — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `airflow` tools
- Tools: `Glob`, `Grep`, `Read`, `Airflow` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `airflow:f4b7c491`

# Airflow

Workflow orchestration: DAG authoring, scheduling, backfills, and troubleshooting
via the Airflow CLI.

## When to Use

- Scheduling ETL and ML pipelines
- Re-running failed or historical ranges (backfill)
- Testing individual tasks without running a full DAG

## Real Commands

```bash
# Install (recommended via pipx/venv)
pip install apache-airflow

# First-time database setup
airflow db init
airflow db upgrade

# Create an admin user
airflow users create --username admin --role Admin --email admin@example.com --firstname Admin --lastname User

# Start services (two terminals)
airflow scheduler
airflow webserver --port 8080

# DAG management
airflow dags list
airflow dags list-import-errors
airflow dags show my_dag

# Trigger a run
airflow dags trigger my_dag --conf '{"env": "staging"}'

# Test one task with a fixed execution date
airflow tasks test my_dag extract 2024-01-01

# Backfill a range
airflow dags backfill -s 2024-01-01 -e 2024-01-10 my_dag --reset-dagruns
```

## Minimal DAG (dags/example.py)

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG("example", start_date=datetime(2024, 1, 1), schedule="@daily", catchup=False) as dag:
    extract = BashOperator(task_id="extract", bash_command="python /app/extract.py")
    load = BashOperator(task_id="load", bash_command="python /app/load.py")
    extract >> load
```

## Best Practices

- Keep DAGs idempotent and deterministic
- Test with `airflow tasks test` before scheduling
- Set proper `start_date` and use catchup deliberately
- Put secrets in Airflow Variables/Connections, not code
- Monitor with `airflow dags list-runs -d my_dag`

## Example Response

For a failed DAG run: identifies the failing task from logs, suggests the fix,
then re-runs the single task or backfills the range.

## Capabilities

### airflow-operations
Manage Airflow metadata, users, DAGs, and task runs from the CLI

**Parameters:**
- `conf` (string): JSON config passed to the triggered run
- `log-level` (string): Logging level for the command, e.g. DEBUG
- `subdir` (string): Directory to search for DAG files

**Commands:**
- `airflow db init`
- `airflow users create --username admin --firstname A --lastname A --role Admin --email admin@localhost`
- `airflow dags list`
- `airflow dags trigger my_dag --conf '{"env": "prod"}'`
- `airflow tasks test my_dag extract_task 2024-01-01`

**Examples:**
- airflow dags list-import-errors
- airflow dags backfill -s 2024-01-01 -e 2024-01-10 my_dag
- airflow scheduler --num-runs 1

## References
- [Airflow docs](https://airflow.apache.org/docs/)
- [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
