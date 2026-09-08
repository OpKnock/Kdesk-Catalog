---
name: "async-task-engineer"
description: "Builds async task systems: Celery and RQ workers for Python, BullMQ queues for Node, Redis brokers, scheduled tasks, and retry policies. Use when working with celery, bullmq node or when the user mentions celery, bullmq node."
type: knowledge
triggers: ["async-task-engineer", "celery", "bullmq-node"]
---

Builds async task systems: Celery and RQ workers for Python, BullMQ queues for Node, Redis brokers, scheduled tasks, and retry policies.

## Agentic Workflow: Read -> Reason -> Act (async-task-engineer)

You are **async-task-engineer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `async-task-engineer`
- Domain: Builds async task systems: Celery and RQ workers for Python, BullMQ queues for Node, Redis brokers, scheduled tasks, and retry policies.
- **celery**: Run Celery tasks with Redis broker — `pip install celery redis`
- **bullmq-node**: Queue async work with BullMQ — `npm install bullmq ioredis`
- Check `knowledge` and `prerequisites: redis, rabbitmq, node.js, python`

### 2. Reason — think for `async-task-engineer`
- For `celery`: Run Celery tasks with Redis broker — decide which checks to run
- For `bullmq-node`: Queue async work with BullMQ — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `async-task-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Celery` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `async-task-engineer:7c6e1c39`

# Async Task Engineer

Async task processing.

## What This Skill Does
- Processes background jobs with Celery/RQ/BullMQ
- Schedules recurring tasks
- Handles retries and failures

## When to Use
- Email and notification sending
- Report generation
- Webhook fan-out

## Real Commands

```bash
pip install celery redis
celery -A tasks worker --loglevel=info -c 4
celery -A tasks beat --loglevel=info
npm install bullmq ioredis
node worker.js
```

## Celery Task

```python
from celery import Celery
app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3)
def send_email(self, to):
    try:
        send(to)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)
```

## Testing
- Enqueue jobs and verify execution
- Test retry behavior on failures
- Monitor queue depths during bursts


## Best Practices
- Keep tasks idempotent
- Set retries with exponential backoff
- Monitor dead-letter queues

## Capabilities

### celery
Run Celery tasks with Redis broker

**Parameters:**
- `app` (string): Celery app module
- `concurrency` (integer): Worker processes
- `queue` (string): Queue name

**Commands:**
- `pip install celery redis`
- `celery -A tasks worker --loglevel=info -c 4`
- `celery -A tasks beat --loglevel=info`
- `celery -A tasks call tasks.send_email --args='["a@localhost"]'`
- `celery -A tasks inspect active`

**Examples:**
- celery worker -c 4 runs 4 worker processes
- celery beat schedules periodic tasks
- celery inspect active lists running tasks

### bullmq-node
Queue async work with BullMQ

**Commands:**
- `npm install bullmq ioredis`
- `node -e "const {Queue}=require('bullmq'); new Queue('jobs').add('email',{to:'a@localhost'},{attempts:3,backoff:{type:'exponential',delay:1000}}).then(j=>console.log('queued',j.id))"`
- `node worker.js`
- `redis-cli ping`
- `rq worker --url redis://localhost:6379`

**Examples:**
- -cli --help
- -api --help

## References
- [Celery Docs](https://docs.celeryq.dev/en/stable/)
- [BullMQ Docs](https://docs.bullmq.io/)
