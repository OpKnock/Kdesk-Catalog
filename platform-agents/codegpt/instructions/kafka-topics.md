# Kafka Topics

Full Kafka topic lifecycle: create with configs, list, describe layout, alter configurations, and delete topics safely with the Kafka CLI.

## Instructions

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

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders --show-configs`
- `kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --config max.message.bytes=2097152`
- `kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --delete-config max.message.bytes`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders
- kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --config max.message.bytes=2097152
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders --show-configs
