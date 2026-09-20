---
name: "async-task-engineer"
description: "Builds async task systems: Celery and RQ workers for Python, BullMQ queues for Node, Redis brokers, scheduled tasks, and retry policies. Use when working with celery, bullmq node or when the user mentions celery, bullmq node."
license: "MIT"
compatibility: "Requires redis, rabbitmq, node.js, python, bull, celery."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(celery:*) Bash(node:*) Bash(npm:*) Bash(pip:*) Bash(redis-cli:*) Bash(rq:*)"
---

Builds async task systems: Celery and RQ workers for Python, BullMQ queues for Node, Redis brokers, scheduled tasks, and retry policies.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install celery redis`, `npm install bullmq ioredis`
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
