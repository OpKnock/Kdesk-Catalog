---
type: agent_requested
description: "Expert Python skill for Redis Streams using redis-py: covers xadd producers, xread/xreadgroup consumers, xack acknowledgments, and xtrim stream maintenance for job queues and replayable logs. Use when working with redis py streams, api or when the user mentions redis py streams, api."
---

Expert Python skill for Redis Streams using redis-py: covers xadd producers, xread/xreadgroup consumers, xack acknowledgments, and xtrim stream maintenance for job queues and replayable logs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install redis`
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

# Redis Streams in Python

Expert skill for Redis Streams with redis-py.

## What this skill does

- Produces entries with xadd and lets Redis generate sequence IDs
- Consumes with xreadgroup in blocking mode for at-least-once delivery
- Acknowledges, inspects pending entries, and trims the stream

## When to use

- Python workers processing job queues stored in streams
- Backfill pipelines that need replayable logs
- Quick data-science reads of stream data

## Real commands

```bash
pip install redis

# Add an entry, returns the new ID
python -c 'import redis; r=redis.Redis(); print(r.xadd("orders", {"sku":"A1","qty":2}))'

# Blocking read of new entries
python -c 'import redis; r=redis.Redis(); print(r.xread({"orders": "$"}, count=1, block=5000))'

# Create a consumer group
python -c 'import redis; r=redis.Redis(); print(r.xgroup_create("orders", "workers", id="$", mkstream=True))'

# Read from a group
python -c 'import redis; r=redis.Redis(); print(r.xreadgroup("workers", "c1", {"orders": ">"}, count=2, block=5000))'

# Pending list and trim
python -c 'import redis; r=redis.Redis(); print(r.xpending("orders", "workers"))'
python -c 'import redis; r=redis.Redis(); print(r.xtrim("orders", maxlen=1000))'
```

## Consumer loop

```python
import redis, time

r = redis.Redis()
while True:
    msgs = r.xreadgroup("workers", "c1", {"orders": ">"}, count=10, block=5000)
    for _, entries in msgs:
        for msg_id, fields in entries:
            print(msg_id, fields)
            r.xack("orders", "workers", msg_id)
```

## Testing

```bash
python -c 'import redis; r=redis.Redis(); print(r.xlen("orders"))'
python -c 'import redis; r=redis.Redis(); print(r.xinfo_groups("orders"))'
```

## Best practices

- Always xack after handling to keep the pending list bounded
- Use id="$" only for new groups; use "0" to replay from the beginning
- Keep the group name stable across deploys so consumption resumes cleanly

## Capabilities

### redis-py-streams
Work with Redis Streams from Python: add, read, group, ack, trim

**Parameters:**
- `block` (integer): Milliseconds to block waiting for a new entry
- `count` (integer): Maximum entries returned per read
- `maxlen` (integer): Trim target for xtrim

**Commands:**
- `pip install redis`
- `python -c 'import redis; r=redis.Redis(); print(r.xadd("orders", {"sku":"A1","qty":2}))'`
- `python -c 'import redis; r=redis.Redis(); print(r.xread({"orders": "$"}, count=1, block=5000))'`
- `python -c 'import redis; r=redis.Redis(); print(r.xgroup_create("orders", "workers", id="$", mkstream=True))'`
- `python -c 'import redis; r=redis.Redis(); print(r.xpending("orders", "workers"))'`

**Examples:**
- python -c 'import redis; r=redis.Redis(); print(r.xrange("orders", count=5))'
- python -c 'import redis; r=redis.Redis(); print(r.xreadgroup("workers", "c1", {"orders": ">"}, count=2, block=5000))'
- python -c 'import redis; r=redis.Redis(); print(r.xtrim("orders", maxlen=1000))'

## References
- [redis-py streams examples](https://redis-py.readthedocs.io/en/stable/examples.html)
- [Redis Streams docs](https://redis.io/docs/latest/develop/data-types/streams/)