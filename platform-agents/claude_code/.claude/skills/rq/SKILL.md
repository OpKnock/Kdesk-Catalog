---
name: "rq"
description: "Runs Redis Queue (RQ) workers and jobs in Python: enqueue, retries, scheduling, dashboards, and worker management. Use when working with rq workers, rq ops, backend or when the user mentions rq workers, rq ops, backend."
license: "MIT"
compatibility: "Requires python."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(python:*) Bash(rq:*)"
---

Runs Redis Queue (RQ) workers and jobs in Python: enqueue, retries, scheduling, dashboards, and worker management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rq worker`, `rq info`
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

# RQ (Redis Queue)

Simple Python task queue backed by Redis.

## When to Use

- Background jobs for Python services already using Redis
- Lightweight alternative to Celery
- Burst processing where worker lifetime is short

## Setup

```bash
pip install rq
```

## Commands

```bash
# Start a worker
rq worker

# Specific queues in priority order
rq worker high default low

# With built-in scheduler
rq worker --with-scheduler

# Burst mode: drain queues and exit
rq worker --burst

# Inspect state
rq info
rq info --only-queues

# Requeue failed jobs
rq requeue --queue failed
```

## Job Example

```python
# tasks.py
import time

def send_email(to, subject):
    time.sleep(1)
    return f"sent to {to}"
```

```python
# enqueue
from redis import Redis
from rq import Queue
from tasks import send_email

q = Queue(connection=Redis())
job = q.enqueue(send_email, "a@b.c", "Hello", retry=Retry(max=3, interval=[10, 60, 300]))
print(job.id)
```

## Best Practices

- Use retry with exponential intervals for flaky work
- Keep one worker per queue group; prioritize with queue lists
- Use --with-scheduler for periodic jobs
- Monitor with rq info and the RQ dashboard
- Set job timeouts explicitly to avoid stuck executions

## Capabilities

### rq-workers
Start and manage RQ worker processes.

**Parameters:**
- `queues` (string): Queue names (space separated)
- `burst` (boolean): Process until queues are empty

**Commands:**
- `rq worker`
- `rq worker --url redis://localhost:6379/1`
- `rq worker --with-scheduler`
- `rq worker high default low`
- `rq worker --name web-worker`

**Examples:**
- rq worker --burst
- rq worker --max-jobs 500
- rq worker -c rq_settings

### rq-ops
Inspect queues and manage jobs from the CLI.

**Parameters:**
- `queue` (string): Queue name
- `job-id` (string): Job identifier

**Commands:**
- `rq info`
- `rq info --only-queues`
- `rq requeue --queue failed`
- `python -c "from rq import Queue; from redis import Redis; q=Queue(\"default\", connection=Redis()); print(q.count)"`
- `rq empty --all`

**Examples:**
- rq info --interval 5
- rq requeue --all
- python -c "from rq.job import Job; from redis import Redis; print(Job.fetch(\"job-id\", connection=Redis()).get_status())"

## References
- [RQ Docs](https://python-rq.org)
- [RQ on GitHub](https://github.com/rq/rq)
