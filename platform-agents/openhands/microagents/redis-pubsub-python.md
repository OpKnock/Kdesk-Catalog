---
name: "redis-pubsub-python"
description: "Publish and subscribe to Redis channels from Python using redis-py: pattern subscriptions with non-blocking get_message polling loops."
type: knowledge
triggers: ["redis-pubsub-python", "redis-py-pubsub"]
---

# Redis Pubsub Python

Publish and subscribe to Redis channels from Python using redis-py: pattern subscriptions with non-blocking get_message polling loops.

## Instructions

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
