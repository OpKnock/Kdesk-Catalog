---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

Pulsar clients in Python: producer/consumer code, pulsar-client wheel, and message schemas.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install pulsar-client`
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
