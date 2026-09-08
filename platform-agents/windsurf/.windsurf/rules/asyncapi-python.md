---
trigger: glob
description: "Generates Python MQTT applications and dataclass models from AsyncAPI documents with the python-paho-template and Modelina. Use when working with python generation, python models, api or when the user mentions python generation, python models, api."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Generates Python MQTT applications and dataclass models from AsyncAPI documents with the python-paho-template and Modelina.

## Agentic Workflow: Read -> Reason -> Act (asyncapi-python)

You are **Asyncapi Python** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `asyncapi-python`
- Domain: Generates Python MQTT applications and dataclass models from AsyncAPI documents with the python-paho-template and Modelina.
- **python-generation**: Generate a Python MQTT app from an AsyncAPI spec. — `npx @asyncapi/generator asyncapi.yaml @asyncapi/python-paho-template -o ./genera`
- **python-models**: Generate Python dataclasses from the spec schema with Modelina. — `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./generated/src/m`
- Check `knowledge` and `prerequisites: npx, pip, python`

### 2. Reason — think for `asyncapi-python`
- For `python-generation`: Generate a Python MQTT app from an AsyncAPI spec. — decide which checks to run
- For `python-models`: Generate Python dataclasses from the spec schema with Modelina. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `asyncapi-python` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `asyncapi-python:8b500e82`

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

**Parameters:**
- `output` (string): Output directory
- `broker` (string): MQTT broker host/port in generated config

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

**Parameters:**
- `output` (string): Models output directory
- `generate_optional` (boolean): Generate Optional[...] fields from nullable schemas

**Commands:**
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./generated/src/models --language Python`
- `python -c "from generated.src.models import OrderCreated; print(OrderCreated)"`
- `python -m py_compile generated/src/models/*.py`

**Examples:**
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language Python --generate-optional
- python -c "from models import OrderCreated; o=OrderCreated(id='x', amount=1.0); print(o)"
- python -m py_compile models/*.py

## References
- [Python Paho Template](https://github.com/asyncapi/python-paho-template)
- [Modelina Python](https://www.asyncapi.com/docs/tools/modelina/languages/Python)
- [paho-mqtt](https://eclipse.dev/paho/files/paho.mqtt.python/html/)
