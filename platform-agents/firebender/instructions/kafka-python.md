Build Kafka producers and consumers in Python with confluent-kafka: SerializingProducer, Consumer groups, and end-to-end event pipelines.

## Agentic Workflow: Read -> Reason -> Act (kafka-python)

You are **Kafka Python** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kafka-python`
- Domain: Build Kafka producers and consumers in Python with confluent-kafka: SerializingProducer, Consumer groups, and end-to-end event pipelines.
- **python-pipeline**: Write Python producers/consumers with confluent-kafka and verify against the broker. — `pip install confluent-kafka`
- **consume-check**: Inspect consumed data and group state from the CLI. — `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --fro`
- Check `knowledge` and `prerequisites: kafka-console-consumer.sh, kafka-consumer-groups.sh, kafka-topics.sh, pip`

### 2. Reason — think for `kafka-python`
- For `python-pipeline`: Write Python producers/consumers with confluent-kafka and verify against the broker. — decide which checks to run
- For `consume-check`: Inspect consumed data and group state from the CLI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka-python` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Kafka-topics.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka-python:a7e0964e`

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
