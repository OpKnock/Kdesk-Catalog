---
name: "kafka"
description: "Core Kafka operations: run a local cluster, manage topics, produce and consume messages, and inspect consumer groups from the command line. Use when working with core cluster, core messaging, api or when the user mentions core cluster, core messaging, api."
license: "MIT"
compatibility: "Requires kafka-broker-api-versions.sh, kafka-console-consumer.sh, kafka-console-producer.sh, kafka-consumer-groups.sh, kafka-server-start.sh, kafka-storage.sh."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(kafka-broker-api-versions.sh:*) Bash(kafka-console-consumer.sh:*) Bash(kafka-console-producer.sh:*) Bash(kafka-consumer-groups.sh:*) Bash(kafka-server-start.sh:*) Bash(kafka-storage.sh:*) Bash(kafka-topics.sh:*)"
---

Core Kafka operations: run a local cluster, manage topics, produce and consume messages, and inspect consumer groups from the command line.

## Agentic Workflow: Read -> Reason -> Act (kafka)

You are **Kafka** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kafka`
- Domain: Core Kafka operations: run a local cluster, manage topics, produce and consume messages, and inspect consumer groups from the command line.
- **core-cluster**: Start and verify a Kafka broker (KRaft mode). — `kafka-server-start.sh config/kraft/server.properties`
- **core-messaging**: Create topics, produce and consume messages, and inspect groups. — `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --part`
- Check `knowledge` and `prerequisites: kafka-broker-api-versions.sh, kafka-console-consumer.sh, kafka-console-producer.sh, kafka-consumer-groups.sh`

### 2. Reason — think for `kafka`
- For `core-cluster`: Start and verify a Kafka broker (KRaft mode). — decide which checks to run
- For `core-messaging`: Create topics, produce and consume messages, and inspect groups. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka` tools
- Tools: `Glob`, `Grep`, `Read`, `Kafka-server-start.sh`, `Kafka-storage.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka:e3793304`

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

**Parameters:**
- `config` (string): Server properties file.

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

**Parameters:**
- `topic` (string): Topic name.
- `partitions` (integer): Partition count.
- `from_beginning` (boolean): Read all historical messages.

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

## References
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Quickstart](https://kafka.apache.org/quickstart)
