# Kafka

Operates Apache Kafka clusters: topic lifecycle, producer/consumer tools, consumer groups, and performance benchmarking.

## Instructions

# Kafka

Operate Kafka with the standard CLI toolchain.

## When to Use

- Event streaming pipelines
- Consumer group debugging
- Topic lifecycle management

## Topics

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 12 --replication-factor 3
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic events
```

Partitions bound parallelism; keep them stable unless growth requires more.

## Produce and consume

```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning
```

## Consumer groups

```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group order-processor --describe
```

Watch LAG; a growing lag with healthy consumers means under-provisioning.

## Offset reset (troubleshooting)

```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group order-processor --reset-offsets --to-earliest --execute
```

Only reset when a consumer bug caused data to be skipped - document first.

## Config tuning

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic events --config retention.ms=604800000
```

## Best practices

- Prefer `--describe` before any alter/delete.
- Use keyed producers to preserve order per key.
- Monitor ISR (in-sync replicas) - under-replicated partitions signal trouble.
- Right-size consumer parallelism to partitions.

## Testing

Produce 10k keyed messages, consume with a group, and verify LAG reaches 0.

## Capabilities

### topics
Create, describe, and alter Kafka topics.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 12 --replication-factor 3`
- `kafka-topics.sh --bootstrap-server localhost:9092 --list`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic events`
- `kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic events --partitions 24`
- `kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic legacy_events`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic events --topics-with-overrides
- kafka-topics.sh --bootstrap-server localhost:9092 --list | grep -v internal
- kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic events --config retention.ms=604800000

### console
Produce and consume messages from the CLI.

**Commands:**
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --group debug-group --property print.offset=true --max-messages 10`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events --property parse.key=true --property key.separator=:`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group debug-group --describe`

**Examples:**
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning --max-messages 5
- echo 'key1:value1' | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events --property parse.key=true --property key.separator=:
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
