# Background Jobs

Designs and operates async background job systems across BullMQ, Celery, and Sidekiq with retries, delays, priorities, and worker lifecycle management.

## Instructions

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

**Commands:**
- `celery -A proj inspect registered`
- `celery -A proj inspect active_queues`
- `redis-cli keys "bull:*"`
- `redis-cli hgetall bull:job:12345`

**Examples:**
- celery -A proj inspect stats
- redis-cli lrange bull:email:wait 0 10