---
trigger: glob
description: "Build Kafka producers and consumers in Python with confluent-kafka: SerializingProducer, Consumer groups, and end-to-end event pipelines. Use when working with python pipeline, consume check, api or when the user mentions python pipeline, consume check, api."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
---

Build Kafka producers and consumers in Python with confluent-kafka: SerializingProducer, Consumer groups, and end-to-end event pipelines.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install confluent-kafka`, `kafka-console-consumer.sh --bootstrap-server localhost:9092 `
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

# Kafka (Python)

Stream events with the confluent-kafka Python client.

## What this skill does

- Produces records with SerializingProducer.
- Consumes in groups with on_assign/on_revoke callbacks.
- Verifies end-to-end delivery with the Kafka CLI.

## When to use

- Python services publishing/consuming events.
- Data pipelines feeding analytics.
- ML feature streams from Kafka topics.

## Real commands

```bash
# Install
pip install confluent-kafka

# Create topic
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic events --partitions 6 --replication-factor 1

# Produce
python producer.py --topic events --count 500

# Consume
python consumer.py --topic events --group analytics

# CLI verification
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic events --from-beginning --max-messages 3
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group analytics
```

## Producer example

```python
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

producer = SerializingProducer({
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': StringSerializer('utf_8'),
    'acks': 'all',
})

producer.produce('events', key='user-1', value='{"action":"click"}')
producer.flush()
```

## Testing

```bash
python -m pytest tests/
```

## Best practices

- Always flush() before exiting to avoid losing buffered messages.
- Set enable.auto.offset.store=false when committing offsets after processing.
- Use librdkafka config keys exactly; unknown keys raise errors.

## Capabilities

### python-pipeline
Write Python producers/consumers with confluent-kafka and verify against the broker.

**Parameters:**
- `topic` (string): Topic name.
- `group` (string): Consumer group id.
- `count` (integer): Messages to produce.

**Commands:**
- `pip install confluent-kafka`
- `python producer.py --topic events --count 500`
- `python consumer.py --topic events --group analytics`
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 6 --replication-factor 1`
- `python -m pytest tests/`

**Examples:**
- python producer.py --topic events --count 500
- python consumer.py --topic events --group analytics
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 6 --replication-factor 1

### consume-check
Inspect consumed data and group state from the CLI.

**Parameters:**
- `reset` (string): auto.offset.reset: earliest or latest.
- `poll` (integer): Poll timeout in milliseconds.

**Commands:**
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning --max-messages 3`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group analytics`
- `python consumer.py --topic events --group analytics --reset earliest --poll 5000`

**Examples:**
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning --max-messages 3
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group analytics
- python consumer.py --topic events --group analytics --reset earliest --poll 5000

## References
- [confluent-kafka-python](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/)
- [confluent_kafka on PyPI](https://pypi.org/project/confluent-kafka/)
