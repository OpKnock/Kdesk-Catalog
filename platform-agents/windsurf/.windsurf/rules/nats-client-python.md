---
trigger: glob
description: "NATS clients in Python with nats-py: async connect, pub/sub, JetStream consumers, and request-reply."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
---

# Nats Client Python

NATS clients in Python with nats-py: async connect, pub/sub, JetStream consumers, and request-reply.

## Instructions

# NATS Python Client

nats-py is the official asyncio-based NATS client for Python.

## What this skill does

- Connects asynchronously with reconnect policies
- Publishes/subscribes and does request-reply
- Consumes from JetStream streams

## When to use

- Python data pipelines and workers
- Async services in the NATS ecosystem

## Real commands

```bash
pip install nats-py
python3 -m pip show nats-py
python3 pub.py
python3 sub.py
```

## Subscribe

```python
import asyncio, nats

async def main():
    nc = await nats.connect("nats://localhost:4222")
    sub = await nc.subscribe("orders.*")
    async for msg in sub:
        print(f"{msg.subject}: {msg.data.decode()}")
        await msg.ack()

asyncio.run(main())
```

## Publish + request

```python
await nc.publish("orders.created", b"{\"id\":1}")
resp = await nc.request("service.echo", b"ping", timeout=2)
print(resp.data)
```

## JetStream consumer

```python
js = nc.jetstream()
pull = await js.pull_subscribe("orders", "worker")
msgs = await pull.fetch(10)
```

## Best practices

- Use `await nc.drain()` on shutdown to flush pending
- Prefer async contexts; avoid blocking calls in the loop
- Use queue groups for competing consumers

## Capabilities

### nats-python-client
Install nats-py and write async Python clients for core NATS and JetStream.

**Commands:**
- `pip install nats-py`
- `python3 -m pip show nats-py`
- `python3 pub.py`
- `python3 sub.py`
- `python3 -c "import nats; print(nats.__version__)"`

**Examples:**
- python3 sub.py
- python3 -m asyncio
- python3 req.py
