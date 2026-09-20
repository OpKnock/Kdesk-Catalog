---
name: "rabbitmq-python"
description: "RabbitMQ clients in Python with pika: connection parameters, blocking adapters, publish/consume and rabbitmqadmin. Use when working with rabbitmq python client, api or when the user mentions rabbitmq python client, api."
type: knowledge
triggers: ["rabbitmq-python", "rabbitmq-python-client"]
---

RabbitMQ clients in Python with pika: connection parameters, blocking adapters, publish/consume and rabbitmqadmin.

## Agentic Workflow: Read -> Reason -> Act (rabbitmq-python)

You are **Rabbitmq Python** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rabbitmq-python`
- Domain: RabbitMQ clients in Python with pika: connection parameters, blocking adapters, publish/consume and rabbitmqadmin.
- **rabbitmq-python-client**: Install pika, write publishers/consumers, and manage queues with rabbitmqadmin. — `pip install pika`
- Check `knowledge` and `prerequisites: pip, python3, rabbitmqadmin`

### 2. Reason — think for `rabbitmq-python`
- For `rabbitmq-python-client`: Install pika, write publishers/consumers, and manage queues with rabbitmqadmin. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rabbitmq-python` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Python3` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rabbitmq-python:5f8d202f`

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
