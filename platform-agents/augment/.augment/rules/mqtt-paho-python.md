---
type: agent_requested
description: "Write MQTT clients in Python with paho-mqtt: connect, publish, subscribe with callbacks, and TLS settings. Use when working with paho python client, api or when the user mentions paho python client, api."
---

Write MQTT clients in Python with paho-mqtt: connect, publish, subscribe with callbacks, and TLS settings.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install paho-mqtt`
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

# Paho MQTT Python

paho-mqtt is the standard Python MQTT client, used in IoT scripts and backend services alike.

## What this skill does

- Installs paho-mqtt and verifies the import
- Writes publish/subscribe scripts with the callback model
- Configures TLS and retained messages

## When to use

- Quick IoT prototypes and data pipelines
- Python services that emit or consume events

## Real commands

```bash
# Install
pip install paho-mqtt
python3 -m pip show paho-mqtt

# Run scripts (write pub.py / sub.py)
python3 pub.py -h localhost -t sensors/temp -m 21.5
python3 sub.py -h localhost -t sensors/#
```

## Publisher

```python
import paho.mqtt.client as mqtt
c = mqtt.Client()
c.connect("localhost", 1883)
c.publish("sensors/temp", "21.5", qos=1)
c.disconnect()
```

## Subscriber with callbacks

```python
def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

c = mqtt.Client()
c.on_message = on_message
c.connect("localhost", 1883)
c.subscribe("sensors/#", qos=0)
c.loop_forever()
```

## TLS

```python
c.tls_set(ca_certs="ca.crt", certfile="client.crt", keyfile="client.key")
c.connect("broker.example.com", 8883)
```

## Best practices

- Call `loop_start()`/`loop_forever()` consistently
- Set a Client ID for persistent sessions
- Keep QoS 0 for telemetry, QoS 1 for events that matter

## Capabilities

### paho-python-client
Install paho-mqtt and build pub/sub clients with the callback-based Python API.

**Parameters:**
- `host` (string): Broker hostname
- `port` (integer): Broker port
- `qos` (integer): QoS level for publish

**Commands:**
- `pip install paho-mqtt`
- `python3 -m pip show paho-mqtt`
- `python3 pub.py -h localhost -t sensors/temp -m 21.5`
- `python3 sub.py -h localhost -t sensors/#`
- `python3 -c "import paho.mqtt.client as mqtt; print(mqtt.__version__ if hasattr(mqtt,'__version__') else 'ok')"`

**Examples:**
- python3 sub.py -h broker.example.com -p 8883 --cafile ca.crt -t '#'
- python3 pub.py -t orders/new -m '{"id":1}' -q 1
- python3 -c "import paho.mqtt.client as mqtt; c=mqtt.Client(); c.connect('localhost',1883); c.publish('t','m'); c.disconnect()"

## References
- [Paho Python docs](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php)
- [paho-mqtt on PyPI](https://pypi.org/project/paho-mqtt/)