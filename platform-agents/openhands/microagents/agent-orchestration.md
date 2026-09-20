---
name: "agent-orchestration"
description: "Orchestrates backend agent and workflow pipelines with Temporal and Apache Airflow: workflow registration, task queues, scheduling, and DAG management. Use when working with temporal, airflow, backend or when the user mentions temporal, airflow, backend."
type: knowledge
triggers: ["agent-orchestration", "temporal", "airflow"]
---

Orchestrates backend agent and workflow pipelines with Temporal and Apache Airflow: workflow registration, task queues, scheduling, and DAG management.

## Agentic Workflow: Read -> Reason -> Act (agent-orchestration)

You are **Agent Orchestration** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `agent-orchestration`
- Domain: Orchestrates backend agent and workflow pipelines with Temporal and Apache Airflow: workflow registration, task queues, scheduling, and DAG management.
- **temporal**: Run and manage Temporal workflows — `temporal server start-dev`
- **airflow**: Author and schedule Airflow DAGs — `pip install apache-airflow`
- Check `knowledge` and `prerequisites: airflow, pip, temporal`

### 2. Reason — think for `agent-orchestration`
- For `temporal`: Run and manage Temporal workflows — decide which checks to run
- For `airflow`: Author and schedule Airflow DAGs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `agent-orchestration` tools
- Tools: `Glob`, `Grep`, `Read`, `Temporal`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `agent-orchestration:1da1b9ea`

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
