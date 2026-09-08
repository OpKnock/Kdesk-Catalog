---
trigger: glob
description: "Operate Kafka log compaction: enable compacted topics, tune min.cleanable.dirty.ratio and segment.ms, and verify tombstones and duplicate-key removal. Use when working with enable compaction, verify compaction, api or when the user mentions enable compaction, verify compaction, api."
globs: ["**/*.r", "**/*.sh"]
---

Operate Kafka log compaction: enable compacted topics, tune min.cleanable.dirty.ratio and segment.ms, and verify tombstones and duplicate-key removal.

## Agentic Workflow: Read -> Reason -> Act (kafka-compaction)

You are **Kafka Compaction** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kafka-compaction`
- Domain: Operate Kafka log compaction: enable compacted topics, tune min.cleanable.dirty.ratio and segment.ms, and verify tombstones and duplicate-key removal.
- **enable-compaction**: Enable and tune log compaction per topic with kafka-configs.sh. — `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity`
- **verify-compaction**: Verify compaction state, log segments, and tombstoned keys. — `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- Check `knowledge` and `prerequisites: kafka-configs.sh, kafka-console-consumer.sh, kafka-log-dirs.sh, kafka-run-class.sh`

### 2. Reason — think for `kafka-compaction`
- For `enable-compaction`: Enable and tune log compaction per topic with kafka-configs.sh. — decide which checks to run
- For `verify-compaction`: Verify compaction state, log segments, and tombstoned keys. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka-compaction` tools
- Tools: `Glob`, `Grep`, `Read`, `Kafka-configs.sh`, `Kafka-topics.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka-compaction:688d5bef`

# Kafka Compaction

Configure and operate Kafka log compaction for keyed, always-latest-value topics.

## What this skill does

- Enables cleanup.policy=compact on topics.
- Tunes compaction frequency (min.cleanable.dirty.ratio) and segment rollover (segment.ms).
- Verifies duplicate keys are removed and tombstones are applied.

## When to use

- Materialized state (user profiles, device registry) stored in Kafka.
- Reduce storage for keyed topics that keep changing.
- Enabling the Kafka Streams changelog compaction requirement.

## Real commands

```bash
# Enable compaction
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name orders --alter \
  --add-config cleanup.policy=compact

# Compact aggressively (lower dirty ratio = more frequent compaction)
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name orders --alter \
  --add-config "min.cleanable.dirty.ratio=0.01"

# Roll segments hourly; keep tombstones 1 day
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name orders --alter \
  --add-config "segment.ms=3600000,delete.retention.ms=86400000"

# Inspect config
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name orders --describe

# Check log segments on disk
kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --topic-list orders

# Read keyed records to verify dedup
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic orders --from-beginning --property print.key=true --max-messages 10
```

## Config example (create with compaction)

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --create \
  --topic user-profiles --partitions 6 --replication-factor 3 \
  --config cleanup.policy=compact --config min.cleanable.dirty.ratio=0.1
```

## Testing

```bash
# Produce a key twice, consume from beginning, expect only the newest value
echo '{"key":"u-1","v":1}' | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic user-profiles --property parse.key=true --property key.separator=:
```

## Best practices

- Compaction works per partition; order is preserved for a key.
- Keep segment.ms small for keyed streams so dirty data rolls over fast.
- Tombstones (null value) remove the key entirely after delete.retention.ms.
- Don't use compacted topics for event logs; use retention-based topics.

## Capabilities

### enable-compaction
Enable and tune log compaction per topic with kafka-configs.sh.

**Parameters:**
- `topic` (string): Topic name to configure.
- `config` (string): Comma-separated configs, e.g. min.cleanable.dirty.ratio=0.01,segment.ms=3600000.

**Commands:**
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --alter --add-config cleanup.policy=compact`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --alter --add-config "min.cleanable.dirty.ratio=0.01"`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --alter --add-config "segment.ms=3600000,delete.retention.ms=86400000"`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --describe`

**Examples:**
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --alter --add-config cleanup.policy=compact
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --alter --add-config "min.cleanable.dirty.ratio=0.01"
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name orders --describe

### verify-compaction
Verify compaction state, log segments, and tombstoned keys.

**Parameters:**
- `topic` (string): Topic to inspect.
- `max_messages` (integer): Number of records to read for verification.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`
- `kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --topic-list orders`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --property print.key=true --max-messages 10`
- `kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic orders --time -1`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --property print.key=true --max-messages 10
- kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --topic-list orders

## References
- [Kafka Log Compaction](https://kafka.apache.org/documentation/#compaction)
- [kafka-configs.sh](https://kafka.apache.org/documentation/#configuration)
