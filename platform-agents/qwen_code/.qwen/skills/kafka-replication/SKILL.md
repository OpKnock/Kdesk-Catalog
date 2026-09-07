---
name: "kafka-replication"
description: "Manage Kafka replica health, trigger leader elections, reassign partitions across brokers, and configure throttle rates. Use when working with replica health, leader and reassign, api or when the user mentions replica health, leader and reassign, api."
license: "MIT"
compatibility: "Requires kafka-configs.sh, kafka-leader-election.sh, kafka-reassign-partitions.sh, kafka-topics.sh."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(kafka-configs.sh:*) Bash(kafka-leader-election.sh:*) Bash(kafka-reassign-partitions.sh:*) Bash(kafka-topics.sh:*)"
---

Manage Kafka replica health, trigger leader elections, reassign partitions across brokers, and configure throttle rates.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-topics.sh --bootstrap-server localhost:9092 --describe`, `kafka-leader-election.sh --bootstrap-server localhost:9092 -`
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
