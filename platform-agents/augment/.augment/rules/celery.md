---
type: agent_requested
description: "Configures and operates Celery distributed task queues: workers, beat scheduler, result backends, routing, and monitoring. Use when working with celery workers, celery beat, backend or when the user mentions celery workers, celery beat, backend."
---

Configures and operates Celery distributed task queues: workers, beat scheduler, result backends, routing, and monitoring.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `celery -A proj worker --loglevel=info`, `celery -A proj beat --loglevel=info`
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

# Celery

Distributed task queue for Python.

## When to Use

- Long-running or I/O-heavy work triggered by web requests
- Periodic jobs via beat
- Retryable processing against flaky external services
- Fan-out jobs across many workers

## Setup

```bash
pip install celery[redis]
```

## Commands

```bash
# Start a worker
celery -A proj worker --loglevel=info

# Multi-queue worker
celery -A proj worker --concurrency=4 -Q high,default

# Periodic scheduler
celery -A proj beat --loglevel=info

# Check worker health
celery -A proj status
celery -A proj inspect active
celery -A proj inspect stats

# Clear pending tasks
celery -A proj purge -f

# Graceful shutdown
celery -A proj control shutdown

# Call a task from the CLI
celery -A proj call tasks.add --args="[2,2]"
```

## Config

```python
# celery.py
from celery import Celery
app = Celery("proj", broker="redis://localhost:6379/0",
             backend="redis://localhost:6379/1")
app.conf.task_routes = {"tasks.send_email": {"queue": "email"}}
app.conf.beat_schedule = {
    "cleanup-every-10m": {
        "task": "tasks.cleanup",
        "schedule": 600.0,
    }
}
```

## Task Example

```python
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, to):
    try:
        send(to)
    except TemporaryFailure as exc:
        raise self.retry(exc=exc)
```

## Best Practices

- Keep tasks idempotent and small
- Use task_routes to separate critical and background queues
- Always bound tasks with max_retries for network-dependent work
- Use inspect and flower for production monitoring
- Use acks_late for at-least-once delivery semantics

## Capabilities

### celery-workers
Start and manage Celery worker processes.

**Parameters:**
- `concurrency` (integer): Worker process count
- `queues` (string): Queues to consume, comma-separated
- `hostname` (string): Worker hostname template

**Commands:**
- `celery -A proj worker --loglevel=info`
- `celery -A proj worker --concurrency=4 -Q high,default`
- `celery -A proj purge -f`
- `celery -A proj status`
- `celery -A proj control shutdown`

**Examples:**
- celery -A proj worker --loglevel=debug --traceback
- celery -A proj worker --hostname=w1@%h --concurrency=8
- celery -A proj inspect stats

### celery-beat
Schedule periodic tasks with the beat scheduler.

**Parameters:**
- `schedule` (string): Path to the persistent schedule db
- `loglevel` (string): Logging level: info, debug, warning

**Commands:**
- `celery -A proj beat --loglevel=info`
- `celery -A proj beat --schedule /var/lib/celerybeat-schedule`
- `celery -A proj call tasks.add --args="[2,2]"`
- `celery -A proj inspect scheduled`

**Examples:**
- celery -A proj beat --loglevel=info --pidfile=/tmp/beat.pid
- celery -A proj call tasks.send_digest --kwargs="{\"user_id\": 7}"

## References
- [Celery Docs](https://docs.celeryq.dev/en/stable/)
- [Celery Best Practices](https://docs.celeryq.dev/en/stable/userguide/tasks.html)