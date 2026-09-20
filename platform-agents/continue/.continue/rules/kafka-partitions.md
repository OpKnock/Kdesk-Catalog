---
name: "Kafka Partitions"
description: "Manage Kafka topic partitions: sizing, expansion via kafka-topics alter, and rebalancing with kafka-reassign-partitions for even data distribution."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Kafka Partitions

Manage Kafka topic partitions: sizing, expansion via kafka-topics alter, and rebalancing with kafka-reassign-partitions for even data distribution.

## Instructions

# Kafka Partitions

Size, expand, and rebalance Kafka topic partitions.

## What this skill does

- Creates topics with the right partition and replica layout.
- Increases partitions safely (never decreases).
- Generates and executes reassignment plans for balanced distribution.

## When to use

- Capacity planning when a topic's throughput grows.
- Rebalancing after adding brokers to the cluster.
- Fixing hotspot brokers with uneven partition counts.

## Real commands

```bash
# Create with sizing
kafka-topics.sh --bootstrap-server localhost:9092 --create \
  --topic orders --partitions 12 --replication-factor 3

# Expand partitions (can only increase)
kafka-topics.sh --bootstrap-server localhost:9092 --alter \
  --topic orders --partitions 24

# Inspect current layout
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders

# Generate reassignment plan to spread across 4 brokers
cat > topics.json <<'EOF'
{"topics":[{"topic":"orders"}],"version":1}
EOF
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --generate --topics-to-move-json-file topics.json --broker-list "1,2,3,4"

# Execute and verify the plan
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json --execute
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json --verify
```

## topics.json / reassignment example

```json
{"topics":[{"topic":"orders"}],"version":1}
```

## Testing

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders | head -20
```

## Best practices

- Partition count is a maximum parallelism ceiling; size for peak, not average.
- Reassign during low traffic; reassignment moves data across the wire.
- Always --verify after --execute and watch for throttled leader movement.

## Capabilities

### partition-sizing
Create and expand partitions with controlled replica placement.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 12 --replication-factor 3`
- `kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --partitions 24`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- `kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --partitions 48 --validate-only`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 12 --replication-factor 3
- kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --partitions 24
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders | grep PartitionCount

### reassignment
Generate and execute partition reassignment plans across brokers.

**Commands:**
- `kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --generate --topics-to-move-json-file topics.json --broker-list "1,2,3,4"`
- `kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --reassignment-json-file reassignment.json --execute`
- `kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --reassignment-json-file reassignment.json --verify`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topics-with-overrides`

**Examples:**
- kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --generate --topics-to-move-json-file topics.json --broker-list "1,2,3,4"
- kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --reassignment-json-file reassignment.json --execute
- kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --reassignment-json-file reassignment.json --verify