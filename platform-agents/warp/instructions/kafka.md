# Kafka

Core Kafka operations: run a local cluster, manage topics, produce and consume messages, and inspect consumer groups from the command line.

## Instructions

# Kafka (Core)

Core Kafka operations for developers and operators.

## What this skill does

- Boots a local KRaft-based Kafka cluster.
- Creates topics and streams messages with the console tools.
- Inspects consumer groups and broker state.

## When to use

- Local development and demos.
- First-time cluster bring-up and smoke tests.
- Teaching the messaging model (topic, partition, offset).

## Real commands

```bash
# Format KRaft storage (one-time)
kafka-storage.sh format -t $(kafka-storage.sh random-uuid) \
  -c config/kraft/server.properties

# Start broker
kafka-server-start.sh config/kraft/server.properties

# Verify broker is up
kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Create a topic
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic events --partitions 3 --replication-factor 1

# Produce (type lines, Ctrl-D to exit)
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events

# Consume from beginning
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic events --from-beginning

# List topics and groups
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

## Producer with keys

```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic events --property parse.key=true --property key.separator=:
```

## Testing

```bash
# End-to-end smoke test
echo 'hello kafka' | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning --max-messages 1
```

## Best practices

- Use partitions >= consumers for parallel processing.
- Name topics <domain>.<event>; document keys and value schemas.
- Stop brokers with kafka-server-stop.sh to flush state cleanly.

## Capabilities

### core-cluster
Start and verify a Kafka broker (KRaft mode).

**Commands:**
- `kafka-server-start.sh config/kraft/server.properties`
- `kafka-storage.sh format -t $(kafka-storage.sh random-uuid) -c config/kraft/server.properties`
- `kafka-server-start.sh config/server.properties`
- `kafka-broker-api-versions.sh --bootstrap-server localhost:9092`

**Examples:**
- kafka-storage.sh format -t $(kafka-storage.sh random-uuid) -c config/kraft/server.properties
- kafka-server-start.sh config/kraft/server.properties
- kafka-broker-api-versions.sh --bootstrap-server localhost:9092

### core-messaging
Create topics, produce and consume messages, and inspect groups.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 3 --replication-factor 1`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning`
- `kafka-topics.sh --bootstrap-server localhost:9092 --list`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 3 --replication-factor 1
- kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning
