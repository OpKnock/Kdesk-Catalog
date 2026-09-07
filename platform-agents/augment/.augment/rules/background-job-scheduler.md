---
type: agent_requested
description: "Architects background job schedulers: cron systems, retry policies, dead-letter handling, and idempotency across frameworks. Use when working with scheduler systems, scheduler resilience or when the user mentions scheduler systems, scheduler resilience."
---

Architects background job schedulers: cron systems, retry policies, dead-letter handling, and idempotency across frameworks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `crontab -e`, `python -c "from celery import Celery; app=Celery(); print(ap`
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

# Background Job Scheduler

Design reliable scheduling for background work.

## When to Use

- Recurring maintenance (cleanup, digests, reports)
- Off-peak batch processing
- Work that must survive process restarts

## Options by Stack

- System: cron / systemd timers for host-level jobs
- Celery: beat scheduler for Python distributed jobs
- RQ: --with-scheduler for Redis-backed periodic jobs
- BullMQ: repeatable jobs with cron expressions
- Sidekiq: sidekiq-cron for Ruby

## Commands

```bash
# Host cron
crontab -e
crontab -l

# systemd timers
systemctl list-timers
systemctl status backup.timer

# Celery beat
celery -A proj beat --loglevel=info

# RQ scheduler
rq worker --with-scheduler

# Inspect failed/dead-letter state
redis-cli llen failed-jobs
redis-cli zrange delayed:jobs 0 -1
```

## Retry Policy

```python
# Exponential backoff with cap
@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def cleanup(self):
    try:
        run_cleanup()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))
```

## Best Practices

- Make every job idempotent; scheduler replays happen
- Add jitter to scheduled times to avoid thundering herd
- Centralize retry/backoff config per job class
- Route poison jobs to a dead-letter queue, never silent drop
- Alert when the scheduler itself has not run (watchdog)
- Keep cron at the host level minimal; prefer app-level scheduling

## Capabilities

### scheduler-systems
Configure cron, systemd timers, and application schedulers.

**Parameters:**
- `schedule` (string): Cron expression
- `backend` (string): Scheduler backend: cron, systemd, beat

**Commands:**
- `crontab -e`
- `crontab -l`
- `systemctl list-timers`
- `celery -A proj beat --loglevel=info`
- `rq worker --with-scheduler`

**Examples:**
- crontab -l | grep backup
- systemctl status backup.timer
- celery -A proj beat --schedule /tmp/beat-schedule.db

### scheduler-resilience
Design retries, idempotency, and dead-letter policies.

**Parameters:**
- `queue` (string): Queue name
- `policy` (string): Retry or dead-letter policy name

**Commands:**
- `python -c "from celery import Celery; app=Celery(); print(app.conf.task_default_queue)"`
- `redis-cli llen failed-jobs`
- `redis-cli zrange delayed:jobs 0 -1`
- `redis-cli get job:result:123`

**Examples:**
- redis-cli llen failed-jobs
- redis-cli lrange failed-jobs 0 20

## References
- [Celery Scheduling](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
- [Cron Manual](https://man7.org/linux/man-pages/man5/crontab.5.html)