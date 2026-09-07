Control Kafka data retention: time/size-based retention configs, segment sizing, record deletion by offset, and log dir verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-configs.sh --bootstrap-server localhost:9092 --entity-`, `kafka-delete-records.sh --bootstrap-server localhost:9092 --`
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

# Kafka Retention

Control how long Kafka keeps data and reclaim disk space safely.

## What this skill does

- Sets retention.ms and retention.bytes per topic.
- Tunes segment.bytes/segment.ms for rollover granularity.
- Deletes records below explicit offsets and verifies log sizes.

## When to use

- Reducing storage cost for high-volume topics.
- Complying with data-retention policies.
- Purging sensitive records immediately (deletion by offset).

## Real commands

```bash
# Retain 30 days (2592000000 ms)
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name audit --alter \
  --add-config retention.ms=2592000000

# Cap size at 1 GiB per partition
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name audit --alter \
  --add-config "retention.bytes=1073741824"

# Roll segments hourly for faster cleanup
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name audit --alter \
  --add-config "segment.bytes=268435456,segment.ms=3600000"

# Show current config
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name audit --describe

# Delete records below an offset
cat > offsets.json <<'EOF'
{"partitions":[{"topic":"audit","partition":0,"offset":500000}],"version":1}
EOF
kafka-delete-records.sh --bootstrap-server localhost:9092 \
  --offset-json-file offsets.json

# Verify log sizes
kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --topic-list audit
```

## Testing

```bash
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 --topic audit --time -1
```

## Best practices

- Retention policy is per segment; segments never partially expire.
- Deletion by offset is a one-way operation; use it deliberately.
- Set log.retention.check.interval.ms on the broker for timely cleanup.

## Capabilities

### retention-config
Set time- and size-based retention per topic with kafka-configs.sh.

**Parameters:**
- `topic` (string): Topic name.
- `retention_ms` (integer): Retention time in milliseconds (30 days = 2592000000).
- `retention_bytes` (integer): Retention size per partition in bytes.

**Commands:**
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name audit --alter --add-config retention.ms=2592000000`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name audit --alter --add-config "retention.bytes=1073741824"`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name audit --alter --add-config "segment.bytes=268435456,segment.ms=3600000"`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name audit --describe`

**Examples:**
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name audit --alter --add-config retention.ms=2592000000
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name audit --alter --add-config "retention.bytes=1073741824"
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name audit --describe

### record-deletion
Delete records below an offset and verify log sizes shrink.

**Parameters:**
- `offsets_file` (string): JSON file with partition->offset pairs to delete below.

**Commands:**
- `kafka-delete-records.sh --bootstrap-server localhost:9092 --offset-json-file offsets.json`
- `kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --topic-list audit`
- `kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic audit --time -1`

**Examples:**
- kafka-delete-records.sh --bootstrap-server localhost:9092 --offset-json-file offsets.json
- kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --topic-list audit

## References
- [Kafka Log Retention](https://kafka.apache.org/documentation/#retention)
- [kafka-delete-records](https://kafka.apache.org/documentation/#basic_ops_delete_records)