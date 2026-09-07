---
name: "rabbitmq-python"
description: "RabbitMQ clients in Python with pika: connection parameters, blocking adapters, publish/consume and rabbitmqadmin. Use when working with rabbitmq python client, api or when the user mentions rabbitmq python client, api."
license: "MIT"
compatibility: "Requires pip, python3, rabbitmqadmin."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(pip:*) Bash(python3:*) Bash(rabbitmqadmin:*)"
---

RabbitMQ clients in Python with pika: connection parameters, blocking adapters, publish/consume and rabbitmqadmin.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install pika`
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

# RabbitMQ Python

pika is the standard Python client for RabbitMQ with blocking and async adapters.

## What this skill does

- Installs pika and connects
- Publishes/consumes with the BlockingConnection
- Manages queues with rabbitmqadmin

## When to use

- Python workers and scripts
- Quick queue prototyping

## Real commands

```bash
pip install pika
python3 publisher.py
python3 consumer.py

# Manage via rabbitmqadmin
rabbitmqadmin declare queue name=tasks durable=true
rabbitmqadmin get queue=tasks --count=5
```

## Publisher

```python
import pika
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
ch = conn.channel()
ch.queue_declare(queue="tasks", durable=True)
ch.basic_publish(exchange="", routing_key="tasks", body="job",
                 properties=pika.BasicProperties(delivery_mode=2))
conn.close()
```

## Consumer

```python
ch.basic_qos(prefetch_count=1)
ch.basic_consume(queue="tasks", on_message_callback=cb)
ch.start_consuming()
```

## Best practices

- Use delivery_mode=2 for durable messages
- Acknowledge explicitly for at-least-once
- Set prefetch_count for fair dispatch

## Capabilities

### rabbitmq-python-client
Install pika, write publishers/consumers, and manage queues with rabbitmqadmin.

**Parameters:**
- `queue` (string): Queue name
- `host` (string): RabbitMQ host
- `durable` (boolean): Survive broker restarts

**Commands:**
- `pip install pika`
- `python3 publisher.py`
- `python3 consumer.py`
- `rabbitmqadmin declare queue name=tasks durable=true`
- `rabbitmqadmin get queue=tasks --count=5`

**Examples:**
- python3 consumer.py
- rabbitmqadmin declare queue name=alerts arguments='{"x-message-ttl":60000}'
- python3 -c "import pika; print(pika.__version__)"

## References
- [Pika GitHub](https://github.com/pika/pika)
- [RabbitMQ Python guide](https://www.rabbitmq.com/clients/pika.html)
