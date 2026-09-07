---
type: agent_requested
description: "Operates Apache Kafka clusters: topic lifecycle, producer/consumer tools, consumer groups, and performance benchmarking. Use when working with topics, console, messaging or when the user mentions topics, console, messaging."
---

Operates Apache Kafka clusters: topic lifecycle, producer/consumer tools, consumer groups, and performance benchmarking.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-topics.sh --bootstrap-server localhost:9092 --create -`, `kafka-console-producer.sh --bootstrap-server localhost:9092 `
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

**Parameters:**
- `partitions` (number): Partition count
- `replication-factor` (number): Replication factor
- `config` (string): Topic config like retention.ms

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

**Parameters:**
- `topic` (string): Topic to produce/consume
- `group` (string): Consumer group id
- `max-messages` (number): Consume N messages then exit

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

## References
- [Kafka Quickstart](https://kafka.apache.org/quickstart)
- [Kafka Operations](https://kafka.apache.org/documentation/#operations)
- [Consumer Groups](https://kafka.apache.org/documentation/#intro_consumers)