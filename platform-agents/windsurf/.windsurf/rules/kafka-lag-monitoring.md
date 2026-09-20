---
trigger: glob
description: "Monitor Kafka consumer lag: describe groups per topic/partition, inspect member assignment, reset offsets safely, and compute end-to-end lag from the CLI."
globs: ["**/*.r", "**/*.sh"]
---

# Kafka Lag Monitoring

Monitor Kafka consumer lag: describe groups per topic/partition, inspect member assignment, reset offsets safely, and compute end-to-end lag from the CLI.

## Instructions

# Kafka Lag Monitoring

Track and manage consumer lag with the official Kafka CLI.

## What this skill does

- Reports per-partition LAG for consumer groups.
- Shows member-to-partition assignment.
- Resets offsets for replay, repairs, and backfills.

## When to use

- Investigating slow consumers and growing lag.
- Rolling back consumers after a bad deployment.
- Calculating end-to-end processing delay.

## Real commands

```bash
# Per-partition lag for one group
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group payments

# Which member owns which partitions
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group payments --members --verbose

# Group state (Stable/PreparingRebalance/Dead)
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group payments --state

# Raw latest offsets
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 --topic orders --time -1

# Reset to earliest (requires no active members)
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --reset-offsets --group payments --topic orders --to-earliest --execute

# Replay from a specific datetime
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --reset-offsets --group payments --topic orders \
  --to-datetime 2026-08-01T00:00:00.000 --execute

# Shift offsets back 100 records
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --reset-offsets --group payments --topic orders --shift-by -100 --execute
```

## Config example (alerting)

```bash
# Poll lag every minute and alert when LAG > 10000
watch -n 60 'kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments'
```

## Testing

```bash
# Dry-run a reset before executing
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --reset-offsets --group payments --topic orders --to-earliest --dry-run
```

## Best practices

- Reset only with the group stopped (members cause -execute to fail).
- Alert on lag growth rate, not just absolute lag.
- Pair lag with max.poll.interval.ms: repeated rebalances inflate lag.

## Capabilities

### lag-inspection
Inspect consumer group lag per partition and per member.

**Commands:**
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments --members --verbose`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments --state`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --all-groups`

**Examples:**
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments --members --verbose
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --all-groups | grep -A2 payments

### offset-ops
Get raw offsets and reset group offsets for replay or repairs.

**Commands:**
- `kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic orders --time -1`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group payments --topic orders --to-earliest --execute`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group payments --topic orders --to-datetime 2026-08-01T00:00:00.000 --execute`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group payments --topic orders --shift-by -100 --execute`

**Examples:**
- kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic orders --time -1
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group payments --topic orders --to-earliest --execute
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group payments --topic orders --shift-by -100 --execute
