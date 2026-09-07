---
trigger: glob
description: "Orchestrates backend agent and workflow pipelines with Temporal and Apache Airflow: workflow registration, task queues, scheduling, and DAG management. Use when working with temporal, airflow, backend or when the user mentions temporal, airflow, backend."
globs: ["**/*.r", "**/*.sh"]
---

Orchestrates backend agent and workflow pipelines with Temporal and Apache Airflow: workflow registration, task queues, scheduling, and DAG management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `temporal server start-dev`, `pip install apache-airflow`
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

# Agent Orchestration

Workflow orchestration for backend agents.

## What This Skill Does
- Orchestrates multi-step workflows
- Schedules DAGs and cron pipelines
- Manages retries and state

## When to Use
- Multi-step agent pipelines
- Scheduled data jobs
- Long-running orchestrations

## Real Commands

```bash
temporal server start-dev
temporal workflow start --task-queue my-queue --type OrderWorkflow --input '{"orderId":"o-1"}'
temporal workflow list --query "WorkflowType='OrderWorkflow'"
airflow db migrate
airflow scheduler
```

## Workflow Pattern
1. Start workflow with typed input
2. Worker executes activity steps
3. Engine retries failures
4. Workflow completes with history

## Testing
- Run workflows against the dev server
- Test failure and retry paths
- Validate DAG schedules in Airflow


## Best Practices
- Keep activities idempotent
- Model business state in workflow history
- Use signals for human-in-the-loop steps

## Capabilities

### temporal
Run and manage Temporal workflows

**Parameters:**
- `task-queue` (string): Task queue name
- `workflow-type` (string): Registered workflow type
- `input` (string): JSON workflow input

**Commands:**
- `temporal server start-dev`
- `temporal workflow start --task-queue my-queue --type OrderWorkflow --input '{"orderId":"o-1"}'`
- `temporal workflow list --query "WorkflowType='OrderWorkflow'"`
- `temporal workflow show --workflow-id o-1-workflow`
- `temporal workflow terminate --workflow-id o-1-workflow --reason 'manual stop'`

**Examples:**
- temporal server start-dev runs a local stack
- workflow start dispatches a workflow
- workflow show displays event history

### airflow
Author and schedule Airflow DAGs

**Commands:**
- `pip install apache-airflow`
- `airflow db migrate`
- `airflow users create --username admin --password admin --role Admin --email admin@localhost.test`
- `airflow scheduler`
- `airflow dags list`

**Examples:**
- general-cli --help
- general-api --help

## References
- [Temporal Docs](https://docs.temporal.io/)
- [Airflow Docs](https://airflow.apache.org/docs/)
