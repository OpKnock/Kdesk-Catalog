---
trigger: glob
description: "Runs lightweight task queues with Huey: in-process or Redis-backed workers, cron scheduling, retries, and lock management. Use when working with huey workers, huey scheduling, backend or when the user mentions huey workers, huey scheduling, backend."
globs: ["**/*.go", "**/*.py", "**/*.r", "**/*.sh"]
---

Runs lightweight task queues with Huey: in-process or Redis-backed workers, cron scheduling, retries, and lock management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `huey_consumer tasks.huey`, `redis-cli llen huey:queue`
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

**Parameters:**
- `workers` (integer): Worker process count
- `threads` (integer): Threads per process
- `queues` (string): Queue names to consume

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

**Parameters:**
- `queue` (string): Queue name
- `pattern` (string): Redis key pattern to scan

**Commands:**
- `redis-cli llen huey:queue`
- `redis-cli hgetall huey:results:123`
- `python -c "from tasks import send_mail; send_mail(\"a@b.c\")"`
- `redis-cli --scan --pattern "huey:*"`

**Examples:**
- redis-cli llen huey:queue
- redis-cli zrange huey:scheduled 0 -1

## References
- [Huey Docs](https://huey.readthedocs.io)
- [Huey on GitHub](https://github.com/coleifer/huey)
