---
name: "pulsar-python"
description: "Pulsar clients in Python: producer/consumer code, pulsar-client wheel, and message schemas. Use when working with pulsar python client, api or when the user mentions pulsar python client, api."
---

Pulsar clients in Python: producer/consumer code, pulsar-client wheel, and message schemas.

## Agentic Workflow: Read -> Reason -> Act (pulsar-python)

You are **Pulsar Python** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-python`
- Domain: Pulsar clients in Python: producer/consumer code, pulsar-client wheel, and message schemas.
- **pulsar-python-client**: Install pulsar-client and build Python producers and consumers. — `pip install pulsar-client`
- Check `knowledge` and `prerequisites: pip, python3`

### 2. Reason — think for `pulsar-python`
- For `pulsar-python-client`: Install pulsar-client and build Python producers and consumers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-python` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Python3` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-python:35982cda`

# Pulsar Python

Produce and consume Pulsar messages in Python with the official client.

## What this skill does

- Installs the client wheel
- Writes producer and consumer scripts
- Handles schemas and acking

## When to use

- Data pipelines in Python
- Quick integrations with Pulsar

## Real commands

```bash
pip install pulsar-client
python3 -m pip show pulsar-client
python3 producer.py
python3 consumer.py
```

## Producer

```python
import pulsar
client = pulsar.Client("pulsar://localhost:6650")
producer = client.create_producer("my-topic")
producer.send(("hello").encode("utf-8"))
client.close()
```

## Consumer

```python
consumer = client.subscribe("my-topic", subscription_name="worker")
while True:
    msg = consumer.receive()
    print(msg.data().decode())
    consumer.acknowledge(msg)
```

## Best practices

- Use JsonSchema for structured data
- Always acknowledge messages after processing
- Close the client on exit to flush pending

## Capabilities

### pulsar-python-client
Install pulsar-client and build Python producers and consumers.

**Parameters:**
- `topic` (string): Topic name
- `subscription` (string): Consumer subscription name
- `service_url` (string): pulsar:// broker URL

**Commands:**
- `pip install pulsar-client`
- `python3 -m pip show pulsar-client`
- `python3 producer.py`
- `python3 consumer.py`
- `python3 -c "import pulsar; print(pulsar.__version__)"`

**Examples:**
- python3 producer.py
- python3 consumer.py
- pip install pulsar-client==3.2.0

## References
- [Pulsar Python client docs](https://pulsar.apache.org/docs/3.0.x/client-libraries-python/)
- [pulsar-client on PyPI](https://pypi.org/project/pulsar-client/)
