---
name: "agent-orchestration"
description: "Orchestrates backend agent and workflow pipelines with Temporal and Apache Airflow: workflow registration, task queues, scheduling, and DAG management."
---

# Agent Orchestration

Orchestrates backend agent and workflow pipelines with Temporal and Apache Airflow: workflow registration, task queues, scheduling, and DAG management.

## Instructions

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
