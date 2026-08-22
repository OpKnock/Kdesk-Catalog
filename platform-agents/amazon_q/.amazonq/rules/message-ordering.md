# Message Ordering

Ensure and verify ordered message delivery in Kafka: single-partition ordering, key-based partitioning, sequence checking, and the pitfalls of partition scaling.

## Instructions

# Message Ordering

Guarantee and verify ordered delivery in Kafka.

## What this skill does

- Sets up topics with the partition layout that preserves order.
- Produces keyed records so keys land in one partition.
- Verifies sequence integrity with consumers and scripts.

## When to use

- Event sourcing where event order matters.
- State-machine events per entity (order lifecycle).
- Auditing whether a pipeline lost or reordered records.

## Real commands

```bash
# Global ordering: single partition
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic events --partitions 1 --replication-factor 1

# Per-key ordering: partition by key
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic orders --partitions 6 --replication-factor 3

# Produce keyed records (key:value)
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic orders --property parse.key=true --property key.separator=:

# Ordering with retries: keep in-flight requests low
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name orders --alter \
  --add-config "max.in.flight.requests.per.connection=1"

# Verify: read with keys
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic orders --from-beginning \
  --property print.key=true --property print.value=true --max-messages 50

# Verify: sequence check via script
python3 check_seq.py events
```

## Producer key example

```bash
# Same key => same partition => preserved order per entity
echo "order-42:created" | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders --property parse.key=true --property key.separator=:
echo "order-42:paid" | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders --property parse.key=true --property key.separator=:
```

## Testing

```bash
# check_seq.py logic: seq must be strictly increasing per (topic, partition, key)
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic events --from-beginning --max-messages 100 | \
  awk -F'[,:]' 'NR>1 && $2 <= prev {print "OUT OF ORDER at " NR} {prev=$2}'
```

## Best practices

- Ordering is per partition only: choose partitions=1 or a stable key.
- Idempotent producers + acks=all avoid duplicates without reordering.
- Never reorder by retrying with a different key; the partition is the order contract.

## Capabilities

### ordering-setup
Configure topics and producers for strict ordering.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 1 --replication-factor 1`
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 3`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders --property parse.key=true --property key.separator=:`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --alter --add-config "max.in.flight.requests.per.connection=1"`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 1 --replication-factor 1
- kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders --property parse.key=true --property key.separator=:
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 3

### ordering-verify
Verify sequence integrity with consumers and scripts.

**Commands:**
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning --max-messages 100`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --property print.key=true --property print.value=true --max-messages 50`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group seq-check`
- `python3 check_seq.py events`

**Examples:**
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning --max-messages 100
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --property print.key=true --property print.value=true --max-messages 50
- python3 check_seq.py events