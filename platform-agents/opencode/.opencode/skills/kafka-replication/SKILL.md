---
name: "kafka-replication"
description: "Manage Kafka replica health, trigger leader elections, reassign partitions across brokers, and configure throttle rates. Use when working with replica health, leader and reassign, api or when the user mentions replica health, leader and reassign, api."
---

Manage Kafka replica health, trigger leader elections, reassign partitions across brokers, and configure throttle rates.

## Agentic Workflow: Read -> Reason -> Act (kafka-replication)

You are **Kafka Replication** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kafka-replication`
- Domain: Manage Kafka replica health, trigger leader elections, reassign partitions across brokers, and configure throttle rates.
- **replica-health**: Inspect replication health: ISR state, under-replicated partitions, and unclean leaders. — `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- **leader-and-reassign**: Trigger leader elections and reassign replicas around failed brokers. — `kafka-leader-election.sh --bootstrap-server localhost:9092 --election-type prefe`
- Check `knowledge` and `prerequisites: kafka-configs.sh, kafka-leader-election.sh, kafka-reassign-partitions.sh, kafka-topics.sh`

### 2. Reason — think for `kafka-replication`
- For `replica-health`: Inspect replication health: ISR state, under-replicated partitions, and unclean leaders. — decide which checks to run
- For `leader-and-reassign`: Trigger leader elections and reassign replicas around failed brokers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka-replication` tools
- Tools: `Glob`, `Grep`, `Read`, `Kafka-topics.sh`, `Kafka-leader-election.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka-replication:0d2abde4`

# Kafka Replication

Operate replication: keep ISRs healthy, fail over leaders, and heal replicas.

## What this skill does

- Detects under-replicated partitions and unclean leader states.
- Runs preferred leader elections.
- Reassigns replicas away from dead brokers with throttling.

## When to use

- Broker outages and recovery.
- Verifying RF=3 actually tolerates failures.
- Rebalancing replicas after adding brokers.

## Real commands

```bash
# Find under-replicated partitions
kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --under-replicated-partitions

# Find partitions with unclean leader elections
kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --unclean-offset-leader-available

# Inspect ISR for a topic
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders

# Preferred leader election (all topics)
kafka-leader-election.sh --bootstrap-server localhost:9092 \
  --election-type preferred --all-topic-partitions

# Single partition election
kafka-leader-election.sh --bootstrap-server localhost:9092 \
  --election-type preferred --topic orders --partition 0

# Reassign replicas off a dead broker (1) onto 2,3,4
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --generate --topics-to-move-json-file topics.json --broker-list "2,3,4"

# Throttle replication during reassignment
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type brokers --entity-name 1 --alter \
  --add-config "leader.replication.throttled.rate=10000000,follower.replication.throttled.rate=10000000"
```

## topics.json example

```json
{"topics":[{"topic":"orders"}],"version":1}
```

## Testing

```bash
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json --verify
```

## Best practices

- Watch ISR shrink as the first sign of broker trouble.
- Set unclean.leader.election.enable=false on critical topics.
- Remove throttle configs after reassignment completes.

## Capabilities

### replica-health
Inspect replication health: ISR state, under-replicated partitions, and unclean leaders.

**Parameters:**
- `topic` (string): Topic to inspect.
- `bootstrap` (string): Bootstrap server address.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --unclean-offset-leader-available`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topics-with-overrides`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders | head -10
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --unclean-offset-leader-available

### leader-and-reassign
Trigger leader elections and reassign replicas around failed brokers.

**Parameters:**
- `election_type` (string): preferred or unclean.
- `brokers` (string): Broker ids for reassignment.
- `throttle_rate` (integer): Replication throttle bytes/sec.

**Commands:**
- `kafka-leader-election.sh --bootstrap-server localhost:9092 --election-type preferred --all-topic-partitions`
- `kafka-leader-election.sh --bootstrap-server localhost:9092 --election-type preferred --topic orders --partition 0`
- `kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --generate --topics-to-move-json-file topics.json --broker-list "1,2,3"`
- `kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --reassignment-json-file reassignment.json --execute`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type brokers --entity-name 1 --alter --add-config "leader.replication.throttled.rate=10000000,follower.replication.throttled.rate=10000000"`

**Examples:**
- kafka-leader-election.sh --bootstrap-server localhost:9092 --election-type preferred --all-topic-partitions
- kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --generate --topics-to-move-json-file topics.json --broker-list "1,2,3"
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type brokers --entity-name 1 --alter --add-config "leader.replication.throttled.rate=10000000"

## References
- [Kafka Replication](https://kafka.apache.org/documentation/#replication)
- [kafka-leader-election.sh](https://kafka.apache.org/documentation/#tools)
