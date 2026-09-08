---
type: agent_requested
description: "Operates Kafka clusters: topics, producers, consumers, consumer groups, and configuration via the Kafka CLI. Use when working with kafka cli, data or when the user mentions kafka cli, data."
---

Operates Kafka clusters: topics, producers, consumers, consumer groups, and configuration via the Kafka CLI.

## Agentic Workflow: Read -> Reason -> Act (kafka-data)

You are **Kafka** (data/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `kafka-data`
- Domain: Operates Kafka clusters: topics, producers, consumers, consumer groups, and configuration via the Kafka CLI.
- **kafka-cli**: Manage topics, produce/consume messages, and inspect consumer groups — `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --part`
- Check `knowledge` and `prerequisites: kafka-configs.sh, kafka-console-consumer.sh, kafka-console-producer.sh, kafka-consumer-groups.sh`

### 2. Reason — think for `kafka-data`
- For `kafka-cli`: Manage topics, produce/consume messages, and inspect consumer groups — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka-data` tools
- Tools: `Glob`, `Grep`, `Read`, `Kafka-topics.sh`, `Kafka-console-producer.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka-data:9a113a64`

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

**Parameters:**
- `partitions` (integer): Number of partitions for a new topic
- `replication-factor` (integer): Replication factor for a new topic
- `from-beginning` (boolean): Consume all messages from the topic start

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

## References
- [Kafka docs](https://kafka.apache.org/documentation/)
- [Kafka operations guide](https://kafka.apache.org/documentation/#operations)