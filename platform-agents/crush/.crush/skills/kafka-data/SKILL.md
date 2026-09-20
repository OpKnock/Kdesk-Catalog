---
name: "kafka-data"
description: "Operates Kafka clusters: topics, producers, consumers, consumer groups, and configuration via the Kafka CLI."
---

# Kafka

Operates Kafka clusters: topics, producers, consumers, consumer groups, and configuration via the Kafka CLI.

## Instructions

# Kafka

Operates Apache Kafka: topic lifecycle, producing/consuming for testing, consumer
group health, and broker config inspection.

## When to Use

- Creating and scaling topics
- Verifying messages flow end-to-end
- Debugging consumer group lag

## Real Commands

```bash
# Topics
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 1
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --partitions 6

# Produce
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders --property parse.key=true --property key.separator=:

# Consume
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --max-messages 10

# Consumer groups
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group payments --describe

# Config
kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --describe
```

## Group Lag Debugging

```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group payments --describe
# Look at LAG: if growing, consumers are too slow - scale or optimize
```

## Best Practices

- Size partitions for throughput; more partitions = more parallelism
- Set replication.factor >= 3 in production
- Never consume from-beginning in production apps
- Monitor consumer lag and alert on growth
- Use `--timeout-ms` with commands to avoid CLI hangs

## Example Response

For a lagging consumer group: describes the group, identifies the partition lag,
and recommends scaling consumers or fixing the slow processing step.

## Capabilities

### kafka-cli
Manage topics, produce/consume messages, and inspect consumer groups

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 1`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group payments --describe`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --describe`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --list
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --max-messages 10
- kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic orders --partitions 6
