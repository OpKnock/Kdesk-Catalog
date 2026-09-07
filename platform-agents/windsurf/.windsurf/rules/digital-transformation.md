---
trigger: glob
description: "Drives digital transformation with real tooling: dbt analytics pipelines, workflow orchestration with Airflow, and data platform migrations. Use when working with analytics engineering, workflow orchestration or when the user mentions analytics engineering, workflow orchestration."
globs: ["**/*.r", "**/*.rs", "**/*.sh"]
---

Drives digital transformation with real tooling: dbt analytics pipelines, workflow orchestration with Airflow, and data platform migrations.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `dbt init analytics_project`, `airflow db migrate`
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

# Digital Transformation Engineering

Modernize operations with data platforms, workflow automation, and measurable adoption.

## What This Skill Does

- Builds analytics engineering stacks with dbt
- Orchestrates data workflows with Airflow/Dagster
- Models adoption metrics and KPIs
- Migrates legacy pipelines to modern warehouses
- Automates reporting with dashboards

## When to Use

- Moving an org from spreadsheets to a data platform
- Standardizing ETL/ELT with versioned models
- Building executive dashboards on trusted data

## Real Commands

```bash
# dbt
dbt init analytics_project
dbt run --select staging
dbt test --select tag:core
dbt build --select +marts
dbt docs generate && dbt docs serve
dbt compile --select models/marts

# Airflow
airflow db migrate
airflow users create --username admin --firstname A --lastname U --role Admin --email a@b.c
airflow dags list
airflow dags trigger etl_pipeline
airflow tasks test etl_pipeline extract 2026-08-10
airflow scheduler

# Dagster
dagster job list
dagster materialize -m myrepo
dagit
```

## Transformation Roadmap

1. Inventory current processes and data sources
2. Stand up a warehouse + dbt models (staging -> marts)
3. Orchestrate dependencies with Airflow DAGs
4. Define KPIs and dashboards
5. Train teams; measure adoption monthly

## Best Practices

- Model for trust: test everything with dbt tests
- Orchestrate with idempotent tasks and retries
- Version data definitions like code
- Start with one high-value process; expand after measurable wins
- Track adoption metrics to justify the platform

## Capabilities

### analytics-engineering
Build and test analytics pipelines with dbt.

**Parameters:**
- `select` (string): Node selection, e.g. staging, +marts
- `project` (string): Project name for dbt init

**Commands:**
- `dbt init analytics_project`
- `dbt run --select staging`
- `dbt test --select tag:core`
- `dbt build --select +marts`
- `dbt docs generate`
- `dbt compile --select models/marts`

**Examples:**
- dbt run --select staging
- dbt test --select tag:core
- dbt docs generate

### workflow-orchestration
Schedule and operate data workflows with Airflow and Dagster.

**Parameters:**
- `dag-id` (string): Airflow DAG id
- `task-id` (string): Task id to test

**Commands:**
- `airflow db migrate`
- `airflow users create --username admin --firstname A --lastname U --role Admin --email a@b.c`
- `airflow dags list`
- `airflow dags trigger etl_pipeline`
- `airflow tasks test etl_pipeline extract 2026-08-10`
- `dagster job list`

**Examples:**
- airflow dags list
- airflow dags trigger etl_pipeline
- airflow tasks test etl_pipeline extract 2026-08-10

## References
- [dbt Documentation](https://docs.getdbt.com/)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [AWS Digital Transformation](https://aws.amazon.com/executive-insights/content/digital-transformation/)
