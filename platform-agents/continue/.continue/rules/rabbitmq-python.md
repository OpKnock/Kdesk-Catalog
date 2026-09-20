---
name: "Rabbitmq Python"
description: "RabbitMQ clients in Python with pika: connection parameters, blocking adapters, publish/consume and rabbitmqadmin."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Rabbitmq Python

RabbitMQ clients in Python with pika: connection parameters, blocking adapters, publish/consume and rabbitmqadmin.

## Instructions

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