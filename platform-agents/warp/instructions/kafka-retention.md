Control Kafka data retention: time/size-based retention configs, segment sizing, record deletion by offset, and log dir verification.

## Agentic Workflow: Read -> Reason -> Act (kafka-retention)

You are **Kafka Retention** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kafka-retention`
- Domain: Control Kafka data retention: time/size-based retention configs, segment sizing, record deletion by offset, and log dir verification.
- **retention-config**: Set time- and size-based retention per topic with kafka-configs.sh. — `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity`
- **record-deletion**: Delete records below an offset and verify log sizes shrink. — `kafka-delete-records.sh --bootstrap-server localhost:9092 --offset-json-file off`
- Check `knowledge` and `prerequisites: kafka-configs.sh, kafka-delete-records.sh, kafka-log-dirs.sh, kafka-run-class.sh`

### 2. Reason — think for `kafka-retention`
- For `retention-config`: Set time- and size-based retention per topic with kafka-configs.sh. — decide which checks to run
- For `record-deletion`: Delete records below an offset and verify log sizes shrink. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka-retention` tools
- Tools: `Glob`, `Grep`, `Read`, `Kafka-configs.sh`, `Kafka-delete-records.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka-retention:eb63be7e`

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
