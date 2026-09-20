---
name: "kafka-topics"
description: "Full Kafka topic lifecycle: create with configs, list, describe layout, alter configurations, and delete topics safely with the Kafka CLI. Use when working with topic lifecycle, topic config, api or when the user mentions topic lifecycle, topic config, api."
---

Full Kafka topic lifecycle: create with configs, list, describe layout, alter configurations, and delete topics safely with the Kafka CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-topics.sh --bootstrap-server localhost:9092 --create -`, `kafka-topics.sh --bootstrap-server localhost:9092 --describe`
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

# Kafka Topics

Manage topics through their full lifecycle with the Kafka CLI.

## What this skill does

- Creates topics with partitions, replication, and configs.
- Describes layout (leader, replicas, ISR) and effective configs.
- Alters and deletes topics safely.

## When to use

- Provisioning topics for new services.
- Auditing partition distribution and config drift.
- Cleaning up legacy topics.

## Real commands

```bash
# Create with configs
kafka-topics.sh --bootstrap-server localhost:9092 --create \
  --topic orders --partitions 6 --replication-factor 3 \
  --config retention.ms=604800000 --config max.message.bytes=1048576

# Create only if absent
kafka-topics.sh --bootstrap-server localhost:9092 --create \
  --topic orders --if-not-exists --partitions 6 --replication-factor 3

# List
kafka-topics.sh --bootstrap-server localhost:9092 --list

# Describe layout
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders

# Show effective configs
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders --show-configs

# Alter a config
kafka-topics.sh --bootstrap-server localhost:9092 --alter \
  --topic orders --config max.message.bytes=2097152

# Remove an override
kafka-topics.sh --bootstrap-server localhost:9092 --alter \
  --topic orders --delete-config max.message.bytes

# Delete (requires delete.topic.enable=true on brokers)
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic orders
```

## Testing

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders | grep PartitionCount
```

## Best practices

- Document partition count and rationale; it caps parallelism.
- Keep overrides explicit and reviewed; use --show-configs in audits.
- Never delete topics holding consumer-group offsets still in use.

## Capabilities

### topic-lifecycle
Create, list, and delete topics.

**Parameters:**
- `topic` (string): Topic name.
- `partitions` (integer): Partition count.
- `replication_factor` (integer): Replication factor.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 3 --config retention.ms=604800000 --config max.message.bytes=1048576`
- `kafka-topics.sh --bootstrap-server localhost:9092 --list`
- `kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic orders`
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --if-not-exists --partitions 6 --replication-factor 3`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 3
- kafka-topics.sh --bootstrap-server localhost:9092 --list | grep orders
- kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic orders

### topic-config
Describe topic layout and alter topic configurations.

**Parameters:**
- `topic` (string): Topic name.
- `config` (string): Config key=value to set or remove.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders --show-configs`
- `kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --config max.message.bytes=2097152`
- `kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --delete-config max.message.bytes`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders
- kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --config max.message.bytes=2097152
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders --show-configs

## References
- [kafka-topics.sh](https://kafka.apache.org/documentation/#basic_ops_add_topic)
- [Topic Configs](https://kafka.apache.org/documentation/#topicconfigs)
