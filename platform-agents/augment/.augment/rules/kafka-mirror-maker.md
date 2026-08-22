---
type: agent_requested
description: "Replicate Kafka clusters with MirrorMaker 2: cluster-to-cluster topology configs, connector management, and cross-cluster topic verification."
---

# Kafka Mirror Maker

Replicate Kafka clusters with MirrorMaker 2: cluster-to-cluster topology configs, connector management, and cross-cluster topic verification.

## Instructions

# Kafka MirrorMaker 2

Replicate topics between Kafka clusters for DR, aggregation, and migration.

## What this skill does

- Runs MirrorMaker 2 in standalone mode from a topology config.
- Creates/replicates topics with the correct remote.prefix naming.
- Verifies replicated data and connector task state.

## When to use

- Disaster recovery: replicate primary to secondary cluster.
- Aggregating multiple clusters into one analytics cluster.
- Cluster migrations with low downtime.

## Real commands

```bash
# Run MM2 standalone
kafka-mirror-maker2.sh --config config/mm2.properties

# Run with offset topic management
kafka-mirror-maker2.sh --config config/mm2.properties --manage-offsets

# Legacy MirrorMaker 1 (single topic set)
kafka-mirror-maker.sh --consumer.config consumer.properties \
  --producer.config producer.properties --whitelist 'orders|payments'

# Verify connectors
curl -s http://localhost:8083/connectors | jq .
curl -s http://localhost:8083/connectors/mm2-primary-secondary/status | jq '.tasks[0].state'

# Verify replicated topics and data on secondary
kafka-topics.sh --bootstrap-server secondary:9092 --list | grep orders
kafka-console-consumer.sh --bootstrap-server secondary:9092 \
  --topic secondary.orders --from-beginning --max-messages 5
```

## mm2.properties example

```properties
clusters = primary, secondary
primary.bootstrap.servers = primary:9092
secondary.bootstrap.servers = secondary:9092

primary->secondary.enabled = true
secondary->primary.enabled = false

replication.factor = 3
checkpoints.topic.replication.factor = 1
heartbeats.topic.replication.factor = 1
offset-syncs.topic.replication.factor = 1

sync.topic.acls.enabled = false
refresh.topics.interval.seconds = 60
```

## Testing

```bash
# Produce on primary, consume on secondary
echo '{"dr":"test"}' | kafka-console-producer.sh --bootstrap-server primary:9092 --topic orders
kafka-console-consumer.sh --bootstrap-server secondary:9092 --topic secondary.orders --from-beginning --max-messages 1
```

## Best practices

- Run MM2 in distributed mode (via connect) for HA.
- Keep replication.factor at cluster defaults; configure offset sync intervals.
- Monitor checkpoint lag; growing checkpoint lag means replication is falling behind.

## Capabilities

### mm2-run
Run MirrorMaker 2 in standalone mode with a topology properties file.

**Commands:**
- `kafka-mirror-maker2.sh --config config/mm2.properties`
- `kafka-mirror-maker2.sh --config config/mm2.properties --manage-offsets`
- `kafka-mirror-maker.sh --consumer.config consumer.properties --producer.config producer.properties --whitelist 'orders|payments'`
- `kafka-mirror-maker.sh --consumer.config consumer.properties --producer.config producer.properties --whitelist '.*' --num.streams 4`

**Examples:**
- kafka-mirror-maker2.sh --config config/mm2.properties
- kafka-mirror-maker.sh --consumer.config consumer.properties --producer.config producer.properties --whitelist 'orders|payments'
- kafka-mirror-maker2.sh --config config/mm2.properties --manage-offsets

### verify-replication
Check MM2 connectors, replicated topics, and consumed data on the target cluster.

**Commands:**
- `curl -s http://localhost:8083/connectors | jq .`
- `curl -s http://localhost:8083/connectors/mm2-primary-secondary/status | jq '.tasks[0].state'`
- `kafka-topics.sh --bootstrap-server secondary:9092 --list | grep orders`
- `kafka-console-consumer.sh --bootstrap-server secondary:9092 --topic secondary.orders --from-beginning --max-messages 5`

**Examples:**
- curl -s http://localhost:8083/connectors/mm2-primary-secondary/status | jq '.tasks[0].state'
- kafka-topics.sh --bootstrap-server secondary:9092 --list | grep -E 'orders|payments'
- kafka-console-consumer.sh --bootstrap-server secondary:9092 --topic secondary.orders --from-beginning --max-messages 5