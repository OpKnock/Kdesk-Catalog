---
name: "kafka"
description: "Core Kafka operations: run a local cluster, manage topics, produce and consume messages, and inspect consumer groups from the command line. Use when working with core cluster, core messaging, api or when the user mentions core cluster, core messaging, api."
license: "MIT"
compatibility: "Requires kafka-broker-api-versions.sh, kafka-console-consumer.sh, kafka-console-producer.sh, kafka-consumer-groups.sh, kafka-server-start.sh, kafka-storage.sh."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(kafka-broker-api-versions.sh:*) Bash(kafka-console-consumer.sh:*) Bash(kafka-console-producer.sh:*) Bash(kafka-consumer-groups.sh:*) Bash(kafka-server-start.sh:*) Bash(kafka-storage.sh:*) Bash(kafka-topics.sh:*)"
---

Core Kafka operations: run a local cluster, manage topics, produce and consume messages, and inspect consumer groups from the command line.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-server-start.sh config/kraft/server.properties`, `kafka-topics.sh --bootstrap-server localhost:9092 --create -`
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
