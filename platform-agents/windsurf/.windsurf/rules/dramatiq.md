---
trigger: glob
description: "Builds and operates Dramatiq task queues with Redis/RabbitMQ brokers, worker CLI, delays, and actor middleware. Use when working with dramatiq workers, dramatiq broker, backend or when the user mentions dramatiq workers, dramatiq broker, backend."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
---

Builds and operates Dramatiq task queues with Redis/RabbitMQ brokers, worker CLI, delays, and actor middleware.

## Agentic Workflow: Read -> Reason -> Act (dramatiq)

You are **dramatiq** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `dramatiq`
- Domain: Builds and operates Dramatiq task queues with Redis/RabbitMQ brokers, worker CLI, delays, and actor middleware.
- **dramatiq-workers**: Run and manage Dramatiq worker processes. — `dramatiq worker tasks:broker`
- **dramatiq-broker**: Inspect broker queues and message state directly. — `redis-cli llen dramatiq:default`
- Check `knowledge` and `prerequisites: dramatiq, python, redis-cli`

### 2. Reason — think for `dramatiq`
- For `dramatiq-workers`: Run and manage Dramatiq worker processes. — decide which checks to run
- For `dramatiq-broker`: Inspect broker queues and message state directly. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `dramatiq` tools
- Tools: `Glob`, `Grep`, `Read`, `Dramatiq`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `dramatiq:c9828ad1`

# Dramatiq

Background task processing for Python using Redis or RabbitMQ.

## When to Use

- Simple, reliable task queues with minimal ceremony
- At-least-once delivery with retries built in
- Parallel CPU and I/O work spread across worker processes
- Where Celery feels heavy; Dramatiq is lighter weight

## Setup

```bash
pip install dramatiq[redis]
```

## Commands

```bash
# Run workers
dramatiq worker tasks:broker

# Scale processes and threads
dramatiq worker --processes 4 --threads 8 tasks:broker

# Consume specific queues
dramatiq worker tasks --queues email,default

# Auto-reload on file changes
dramatiq worker --watch . tasks

# Inspect queues in Redis
redis-cli llen dramatiq:default
redis-cli lrange dramatiq:default 0 10
redis-cli zrange dramatiq:delayed 0 -1
```

## Actor Example

```python
# tasks.py
import dramatiq
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker(host="localhost")
dramatiq.set_broker(broker)

@dramatiq.actor(max_retries=5, time_limit=60000)
def send_welcome(user_id):
    email = fetch_user(user_id).email
    send_mail(email, "Welcome!")
```

## Enqueue

```python
from tasks import send_welcome
send_welcome.send(42)
send_welcome.send_with_options(args=(42,), delay=3600000)
```

## Best Practices

- Set max_retries and time_limit on every actor
- Keep messages small; pass IDs rather than objects
- Use separate queues for latency-sensitive work
- Run workers under a process manager with at least 2 processes
- Use --watch in dev for fast iteration

## Capabilities

### dramatiq-workers
Run and manage Dramatiq worker processes.

**Parameters:**
- `processes` (integer): Worker process count
- `threads` (integer): Threads per process
- `queues` (string): Queues to consume

**Commands:**
- `dramatiq worker tasks:broker`
- `dramatiq worker --processes 4 --threads 8 tasks:broker`
- `dramatiq worker tasks --queues email,default`
- `dramatiq worker --watch . tasks`
- `python -m dramatiq tasks:broker`

**Examples:**
- dramatiq worker --processes 2 tasks:broker
- dramatiq worker tasks --queues high
- dramatiq worker --watch tasks -v

### dramatiq-broker
Inspect broker queues and message state directly.

**Parameters:**
- `queue` (string): Queue name to inspect
- `pattern` (string): Redis key pattern to scan

**Commands:**
- `redis-cli llen dramatiq:default`
- `redis-cli zrange dramatiq:delayed 0 -1`
- `redis-cli lrange dramatiq:default 0 10`
- `redis-cli flushdb`

**Examples:**
- redis-cli llen dramatiq:email
- redis-cli hgetall dramatiq:message-state

## References
- [Dramatiq Docs](https://dramatiq.io/)
- [Dramatiq Examples](https://dramatiq.io/examples.html)
