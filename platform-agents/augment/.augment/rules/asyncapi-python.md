---
type: agent_requested
description: "Generates Python MQTT applications and dataclass models from AsyncAPI documents with the python-paho-template and Modelina."
---

# Asyncapi Python

Generates Python MQTT applications and dataclass models from AsyncAPI documents with the python-paho-template and Modelina.

## Instructions

# AsyncAPI Python

## What this skill does

Generates Python MQTT applications from AsyncAPI documents with the python-paho-template: publishers, subscribers, requirements, and tests, plus dataclass models from Modelina.

## When to use

- Bootstrapping a Python MQTT worker from a spec
- Generating dataclasses for event payloads
- Keeping Python consumers in sync with an evolving spec

## Real commands

```bash
# Generate the MQTT app
npx @asyncapi/generator asyncapi.yaml @asyncapi/python-paho-template -o ./generated --force-write

# Install and run
pip install -r generated/requirements.txt
python generated/subscriber.py

# Publish a test message
python generated/publisher.py

# Run generated tests
python -m unittest discover -s generated/tests -v

# Generate dataclass models
npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language Python
python -c "from models import OrderCreated; print(OrderCreated(id='a1', amount=12.5))"
```

## Generated files

- publisher.py / subscriber.py - MQTT entry points
- requirements.txt - pinned paho-mqtt
- config.ini - broker host/port/topic settings

## Testing

- Start mosquitto (or docker eclipse-mosquitto), run subscriber, run publisher, assert the message arrives
- Unit-test payload parsing with the generated dataclasses

## Best practices

- Edit broker settings in config, not generated code
- Pin paho-mqtt in requirements.txt
- Regenerate in CI and diff to catch schema drift

## Capabilities

### python-generation
Generate a Python MQTT app from an AsyncAPI spec.

**Commands:**
- `npx @asyncapi/generator asyncapi.yaml @asyncapi/python-paho-template -o ./generated`
- `pip install -r generated/requirements.txt`
- `python generated/publisher.py`
- `python generated/subscriber.py`
- `python -m unittest discover -s generated/tests`

**Examples:**
- npx @asyncapi/generator asyncapi.yaml @asyncapi/python-paho-template -o ./generated --force-write
- pip install -r generated/requirements.txt && python generated/subscriber.py
- python -m unittest discover -s generated/tests -v

### python-models
Generate Python dataclasses from the spec schema with Modelina.

**Commands:**
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./generated/src/models --language Python`
- `python -c "from generated.src.models import OrderCreated; print(OrderCreated)"`
- `python -m py_compile generated/src/models/*.py`

**Examples:**
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language Python --generate-optional
- python -c "from models import OrderCreated; o=OrderCreated(id='x', amount=1.0); print(o)"
- python -m py_compile models/*.py