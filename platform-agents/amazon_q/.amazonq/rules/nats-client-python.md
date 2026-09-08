NATS clients in Python with nats-py: async connect, pub/sub, JetStream consumers, and request-reply.

## Agentic Workflow: Read -> Reason -> Act (nats-client-python)

You are **Nats Client Python** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `nats-client-python`
- Domain: NATS clients in Python with nats-py: async connect, pub/sub, JetStream consumers, and request-reply.
- **nats-python-client**: Install nats-py and write async Python clients for core NATS and JetStream. — `pip install nats-py`
- Check `knowledge` and `prerequisites: pip, python3`

### 2. Reason — think for `nats-client-python`
- For `nats-python-client`: Install nats-py and write async Python clients for core NATS and JetStream. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nats-client-python` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Python3` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nats-client-python:751dc6a5`

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

**Parameters:**
- `url` (string): Server URL including user/pass if needed
- `subject` (string): Subject or wildcard filter
- `queue` (string): Queue group name

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

## References
- [nats.py GitHub](https://github.com/nats-io/nats.py)
- [nats-py on PyPI](https://pypi.org/project/nats-py/)