# celery

Configures and operates Celery distributed task queues: workers, beat scheduler, result backends, routing, and monitoring.

## Instructions

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

**Commands:**
- `celery -A proj beat --loglevel=info`
- `celery -A proj beat --schedule /var/lib/celerybeat-schedule`
- `celery -A proj call tasks.add --args="[2,2]"`
- `celery -A proj inspect scheduled`

**Examples:**
- celery -A proj beat --loglevel=info --pidfile=/tmp/beat.pid
- celery -A proj call tasks.send_digest --kwargs="{\"user_id\": 7}"
