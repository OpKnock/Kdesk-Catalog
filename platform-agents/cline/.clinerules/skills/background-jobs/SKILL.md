---
name: "background-jobs"
description: "Designs and operates async background job systems across BullMQ, Celery, and Sidekiq with retries, delays, priorities, and worker lifecycle management. Use when working with job queues, job monitoring, backend or when the user mentions job queues, job monitoring, backend."
license: "MIT"
compatibility: "Requires celery, redis-cli, sidekiq."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(celery:*) Bash(redis-cli:*) Bash(sidekiq:*)"
---

Designs and operates async background job systems across BullMQ, Celery, and Sidekiq with retries, delays, priorities, and worker lifecycle management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `celery -A proj worker --loglevel=info --concurrency=4`, `celery -A proj inspect registered`
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

# Background Jobs

Build and operate async background job pipelines with BullMQ, Celery, and Sidekiq.

## When to Use

- Offloading slow work (email, video encoding, report generation) from request path
- Scheduled or recurring tasks (cron-like) with Beat or a scheduler
- Fan-out fan-in workflows with dependencies between jobs
- Retry and dead-letter handling for unreliable downstream services

## Core Concepts

- Queue: durable list of pending jobs backed by Redis
- Worker: process that pops jobs and executes the task function
- Broker: transport (Redis, RabbitMQ) that stores jobs and results
- Retry policy: exponential backoff with max retries per task
- Priority and delay: jobs can be scheduled for later or weighted

## Commands

```bash
# Celery worker with 4 processes
celery -A proj worker --loglevel=info --concurrency=4

# Start the periodic scheduler
celery -A proj beat --loglevel=info

# Purge all pending jobs
celery -A proj purge -f

# Inspect running workers
celery -A proj inspect active
celery -A proj inspect registered
celery -A proj status

# Sidekiq worker with weighted queues
sidekiq -C config/sidekiq.yml -q default,5 -q mailers,3

# BullMQ worker (Node.js)
node worker.js

# Inspect BullMQ queue depth in Redis
redis-cli llen bull:email:wait
```

## Task Definition

```python
# tasks.py (Celery)
from celery import shared_task

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, to, subject):
    try:
        send_mail(to, subject)
    except Exception as exc:
        raise self.retry(exc=exc)
```

## Scheduling

```python
# Periodic tasks with beat
from celery.schedules import crontab
beat_schedule = {
    "daily-report": {
        "task": "tasks.generate_report",
        "schedule": crontab(hour=7, minute=30),
    }
}
```

## Best Practices

- Always set max_retries and default_retry_delay to avoid infinite retries
- Use separate queues for critical and low-priority work
- Make tasks idempotent so replay is safe after a crash
- Monitor queue depth and stale jobs in production
- Keep task payloads small; pass IDs, not full objects
- Use result backends only when the caller needs the return value

## Capabilities

### job-queues
Create queues, run workers, and manage job lifecycle across BullMQ, Celery, and Sidekiq.

**Parameters:**
- `concurrency` (integer): Number of worker processes to spawn
- `queues` (string): Comma-separated queue names to process
- `loglevel` (string): Logging level: info, debug, warning, error

**Commands:**
- `celery -A proj worker --loglevel=info --concurrency=4`
- `celery -A proj purge -f`
- `celery -A proj inspect active`
- `sidekiq -C config/sidekiq.yml`
- `redis-cli llen bull:email:wait`

**Examples:**
- celery -A proj worker --loglevel=info --concurrency=4
- sidekiq -C config/sidekiq.yml -q default,5 -q mailers,3
- redis-cli zrange bull:email:delayed 0 -1

### job-monitoring
Inspect queue depth, stalled jobs, and retry state.

**Parameters:**
- `job-id` (string): Job identifier to inspect
- `queue` (string): Queue name to inspect

**Commands:**
- `celery -A proj inspect registered`
- `celery -A proj inspect active_queues`
- `redis-cli keys "bull:*"`
- `redis-cli hgetall bull:job:12345`

**Examples:**
- celery -A proj inspect stats
- redis-cli lrange bull:email:wait 0 10

## References
- [BullMQ Docs](https://docs.bullmq.io)
- [Celery Docs](https://docs.celeryq.dev/en/stable/)
- [Sidekiq Docs](https://github.com/sidekiq/sidekiq/wiki)
