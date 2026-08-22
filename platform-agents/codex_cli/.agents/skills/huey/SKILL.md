---
name: "huey"
description: "Runs lightweight task queues with Huey: in-process or Redis-backed workers, cron scheduling, retries, and lock management."
---

# huey

Runs lightweight task queues with Huey: in-process or Redis-backed workers, cron scheduling, retries, and lock management.

## Instructions

# Huey

Lightweight task queue for Python.

## When to Use

- Simple apps needing background tasks without Celery overhead
- Redis-backed or even in-process queues
- Cron-style scheduling with the built-in crontab support
- Atomic locks for guarding shared resources

## Setup

```bash
pip install huey[redis]
```

## Commands

```bash
# Start the consumer
huey_consumer tasks.huey

# 4 worker processes
huey_consumer tasks.huey -w 4

# Thread pool with 8 threads
huey_consumer tasks.huey -k thread --threads 8

# Debug logging
huey_consumer tasks.huey -l debug

# Inspect queues
redis-cli llen huey:queue
redis-cli --scan --pattern "huey:*"
```

## Task Example

```python
# tasks.py
from huey import RedisHuey
from huey.contrib.djhuey import task  # Django users

huey = RedisHuey("myapp")

@huey.task(retries=3, retry_delay=10)
def send_email(to, subject):
    send(to, subject)

@huey.periodic_task(huey.crontab(minute="0", hour="6"))
def daily_report():
    generate_report()
```

## Enqueue

```python
from tasks import send_email
send_email("user@example.com", "Hello")
```

## Best Practices

- Set retries and retry_delay on tasks touching external services
- Use lock_task for idempotent periodic jobs
- Choose thread or process worker types per task workload
- Monitor huey:queue length to size workers
- Keep the consumer running under a process manager

## Capabilities

### huey-workers
Run Huey consumers for Redis or in-memory brokers.

**Commands:**
- `huey_consumer tasks.huey`
- `huey_consumer tasks.huey -w 4`
- `huey_consumer tasks.huey --workers 2 --threads 8`
- `python -m huey.consumer tasks.huey`
- `redis-cli keys "huey*"`

**Examples:**
- huey_consumer tasks.huey -k thread
- huey_consumer tasks.huey -w 4 -l debug
- huey_consumer tasks.huey --queues default,email

### huey-scheduling
Schedule periodic tasks and manage task state.

**Commands:**
- `redis-cli llen huey:queue`
- `redis-cli hgetall huey:results:123`
- `python -c "from tasks import send_mail; send_mail(\"a@b.c\")"`
- `redis-cli --scan --pattern "huey:*"`

**Examples:**
- redis-cli llen huey:queue
- redis-cli zrange huey:scheduled 0 -1
