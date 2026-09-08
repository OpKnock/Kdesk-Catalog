---
name: "Api Analytics Streaming"
description: "Real-time streaming API analytics with Kafka and ClickHouse - stream API events, aggregate with windowing, and query dashboards live. Use when working with streaming analytics or when the user mentions streaming analytics."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

Real-time streaming API analytics with Kafka and ClickHouse - stream API events, aggregate with windowing, and query dashboards live.

## Agentic Workflow: Read -> Reason -> Act (api-analytics-streaming)

You are **Api Analytics Streaming** (sre) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `api-analytics-streaming`
- Domain: Real-time streaming API analytics with Kafka and ClickHouse - stream API events, aggregate with windowing, and query dashboards live.
- **streaming-analytics**: Stream API events and run real-time aggregations — `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic api-events --`
- Check `knowledge` and `prerequisites: prometheus, grafana, elasticsearch`

### 2. Reason — think for `api-analytics-streaming`
- For `streaming-analytics`: Stream API events and run real-time aggregations — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-analytics-streaming` tools
- Tools: `Glob`, `Grep`, `Read`, `Kafka-topics.sh`, `Kafka-console-producer.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-analytics-streaming:a165fab5`

# API Analytics (Real-time Streaming)

## What this skill does
Stream API events in real time: produce events to Kafka, ingest into ClickHouse, and query windowed aggregations for live dashboards.

## When to use
- Live dashboards with second-level freshness
- High-volume event ingestion (millions/day)
- Time-series analysis with SQL

## Real commands
```bash
# Create the topic
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic api-events --partitions 6 --replication-factor 1

# Produce events from a JSONL file
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic api-events < events.jsonl

# Verify consumption
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic api-events --from-beginning --max-messages 5

# Start ClickHouse
docker run -d -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server

# Create the events table
curl -s -X POST 'http://localhost:8123/?query=CREATE%20TABLE%20IF%20NOT%20EXISTS%20api_events%20(time%20DateTime,%20endpoint%20String,%20status%20UInt16)%20ENGINE%3DMergeTree%20ORDER%20BY%20time'

# Events per minute, last rows
curl -s -X POST 'http://localhost:8123/?query=SELECT%20toStartOfMinute(time)%20as%20m,%20count()%20FROM%20api_events%20GROUP%20BY%20m%20ORDER%20BY%20m%20DESC%20LIMIT%205' | column -t

# Status distribution last 10 minutes
curl -s 'http://localhost:8123/?query=SELECT%20status,%20count()%20FROM%20api_events%20WHERE%20time%20%3E%20now()-600%20GROUP%20BY%20status'
```

## Pipeline
```
API -> Kafka (api-events) -> ClickHouse -> dashboards
```

## Best practices
- Partition by API key or endpoint for parallelism
- Use MergeTree ordering by time for range scans
- Batch inserts (min 1000 rows) for throughput
- Monitor consumer lag with kafka-consumer-groups

## Testing
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic api-events --max-messages 1
curl -s 'http://localhost:8123/?query=SELECT%20count()%20FROM%20api_events'
```

## Capabilities

### streaming-analytics
Stream API events and run real-time aggregations

**Parameters:**
- `topic` (string): Kafka topic for events
- `query` (string): SQL against ClickHouse
- `window` (string): Window function, e.g. toStartOfMinute

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic api-events --partitions 6 --replication-factor 1`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic api-events < events.jsonl`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic api-events --from-beginning --max-messages 5`
- `docker run -d -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server`
- `curl -s -X POST 'http://localhost:8123/?query=SELECT%20toStartOfMinute(time)%20as%20m,%20count()%20FROM%20api_events%20GROUP%20BY%20m%20ORDER%20BY%20m%20DESC%20LIMIT%205' | column -t`

**Examples:**
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic api-events --property print.key=true --max-messages 10
- curl -s 'http://localhost:8123/?query=SELECT%20status,%20count()%20FROM%20api_events%20WHERE%20time%20%3E%20now()-600%20GROUP%20BY%20status'
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group analytics --describe

## References
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [ClickHouse Docs](https://clickhouse.com/docs)