Operates Kafka clusters: topics, producers, consumers, consumer groups, and configuration via the Kafka CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-topics.sh --bootstrap-server localhost:9092 --create -`
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