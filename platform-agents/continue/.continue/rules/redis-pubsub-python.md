---
name: "Redis Pubsub Python"
description: "Publish and subscribe to Redis channels from Python using redis-py: pattern subscriptions with non-blocking get_message polling loops. Use when working with redis py pubsub, api or when the user mentions redis py pubsub, api."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Publish and subscribe to Redis channels from Python using redis-py: pattern subscriptions with non-blocking get_message polling loops.

## Agentic Workflow: Read -> Reason -> Act (redis-pubsub-python)

You are **Redis Pubsub Python** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `redis-pubsub-python`
- Domain: Publish and subscribe to Redis channels from Python using redis-py: pattern subscriptions with non-blocking get_message polling loops.
- **redis-py-pubsub**: Publish and subscribe from Python with the redis-py PubSub object — `pip install redis`
- Check `knowledge` and `prerequisites: pip, python, redis-cli`

### 2. Reason — think for `redis-pubsub-python`
- For `redis-py-pubsub`: Publish and subscribe from Python with the redis-py PubSub object — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-pubsub-python` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-pubsub-python:ae0daead`

# Redis Pub/Sub in Python

Hand-crafted skill for Redis publish/subscribe with redis-py.

## What this skill does

- Publishes messages to channels and checks the subscriber count return value
- Subscribes with non-blocking get_message(timeout=...) polling loops
- Matches multiple channels with psubscribe glob patterns

## When to use

- Broadcasting cache-invalidation events to web workers
- Lightweight event bus between Python services
- Debugging why a subscriber is not receiving messages

## Real commands

```bash
# Install the client
pip install redis

# Publish; prints the number of subscribers that received it
python -c 'import redis; r=redis.Redis(); print(r.publish("news", "breaking"))'

# Subscribe and poll for up to 3 seconds
python -c 'import redis; p=redis.Redis().pubsub(); p.subscribe("news"); print(p.get_message(timeout=3))'

# Pattern subscribe
python -c 'import redis; p=redis.Redis().pubsub(); p.psubscribe("orders.*"); print(p.get_message(timeout=3))'

# CLI counterpart for testing
redis-cli subscribe news
redis-cli publish news "second message"
```

## Listener loop

```python
import redis

r = redis.Redis()
p = r.pubsub()
p.subscribe("news")
for msg in p.listen():
    if msg["type"] == "message":
        print(msg["channel"], msg["data"])
```

## Testing

```bash
# Terminal A: subscriber loop
python listener.py
# Terminal B: publisher
redis-cli publish news "hello from cli"
```

## Best practices

- Call p.close() before process exit to avoid lingering connections
- Ignore the initial subscribe confirmation message in listen() by type check
- Prefer one shared connection pool when many threads publish

## Capabilities

### redis-py-pubsub
Publish and subscribe from Python with the redis-py PubSub object

**Parameters:**
- `timeout` (integer): get_message polling timeout in seconds before returning None
- `channel` (string): Channel name for subscribe()
- `pattern` (string): Glob pattern for psubscribe(), e.g. orders.*

**Commands:**
- `pip install redis`
- `python -c 'import redis; r=redis.Redis(host="localhost", port=6379); print(r.publish("news", "breaking"))'`
- `python -c 'import redis; r=redis.Redis(); p=r.pubsub(); p.subscribe("news"); print(p.get_message(timeout=3))'`
- `redis-cli subscribe news`
- `redis-cli psubscribe orders.*`

**Examples:**
- python -c 'import redis; r=redis.Redis(); print(r.publish("news", "hello"))'
- python -c 'import redis; p=redis.Redis().pubsub(); p.psubscribe("orders.*"); print(p.get_message(timeout=3))'
- redis-cli publish news "second message"

## References
- [redis-py repository](https://github.com/redis/redis-py)
- [Redis pub/sub documentation](https://redis.io/docs/latest/develop/data-types/pubsub/)