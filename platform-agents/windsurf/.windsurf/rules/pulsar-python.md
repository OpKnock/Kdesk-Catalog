---
trigger: glob
description: "Pulsar clients in Python: producer/consumer code, pulsar-client wheel, and message schemas."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

# Pulsar Python

Pulsar clients in Python: producer/consumer code, pulsar-client wheel, and message schemas.

## Instructions

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
