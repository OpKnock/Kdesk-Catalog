---
type: agent_requested
description: "Runs Spark Structured Streaming jobs with Kafka sources. Submits streaming applications locally or in cluster mode on Kubernetes, explores streaming APIs interactively in spark-shell, and tunes aggregation parallelism with shuffle partitions. Use when working with structured streaming, api or when the user mentions structured streaming, api."
---

Runs Spark Structured Streaming jobs with Kafka sources. Submits streaming applications locally or in cluster mode on Kubernetes, explores streaming APIs interactively in spark-shell, and tunes aggregation parallelism with shuffle partitions.

## Agentic Workflow: Read -> Reason -> Act (spark-streaming)

You are **Spark Streaming** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `spark-streaming`
- Domain: Runs Spark Structured Streaming jobs with Kafka sources. Submits streaming applications locally or in cluster mode on Kubernetes, explores streaming APIs interactively in spark-shell, and tunes aggreg
- **structured-streaming**: Runs Spark Structured Streaming jobs with Kafka sources. Submits streaming applications locally or i — `spark-submit --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_`
- Check `knowledge` and `prerequisites: kafka-console-producer, spark-shell, spark-submit`

### 2. Reason — think for `spark-streaming`
- For `structured-streaming`: Runs Spark Structured Streaming jobs with Kafka sources. Submits streaming applications locally or in cluster mode on Ku — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `spark-streaming` tools
- Tools: `Glob`, `Grep`, `Read`, `Spark-submit`, `Spark-shell` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `spark-streaming:fbc07060`

# Spark Structured Streaming

Hand-crafted skill for streaming data pipelines with Spark Structured Streaming.

## What this skill does

- Runs streaming jobs with spark-submit against Kafka topics
- Explores streaming APIs interactively in spark-shell
- Deploys in cluster mode to YARN or Kubernetes

## When to use

- Aggregating event streams with windowing and watermarks
- Joining a stream with a lookup table
- Replacing stateful Kafka consumer microservices

## Real commands

```bash
# Local run with the Kafka connector
spark-submit --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 streaming.py

# Cluster mode on Kubernetes
spark-submit --deploy-mode cluster --master k8s://https://cluster:6443 --class com.app.StreamJob app.jar

# Interactive exploration
spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1

# Tune aggregation parallelism
spark-submit --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 --conf spark.sql.shuffle.partitions=200 streaming.py

# Produce test data
kafka-console-producer --broker-list localhost:9092 --topic events
```

## Streaming job

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, window, col

spark = SparkSession.builder.appName("events").getOrCreate()
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "events")
    .option("startingOffsets", "earliest")
    .load()
)
counts = df.groupBy(window(col("ts"), "1 minute")).count()
counts.writeStream.outputMode("update").format("console").start().awaitTermination()
```

## Testing

```bash
kafka-console-producer --broker-list localhost:9092 --topic events <<< '{"ts":"2026-08-10T10:00:00Z","value":1}'
spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 streaming.py
```

## Best practices

- Pin the spark-sql-kafka artifact version to your Spark version
- Use checkpointLocation on durable storage for exactly-once recovery
- Set startingOffsets=earliest for backfill, latest for production tailing

## Capabilities

### structured-streaming
Runs Spark Structured Streaming jobs with Kafka sources. Submits streaming applications locally or in cluster mode on Kubernetes, explores streaming APIs interactively in spark-shell, and tunes aggregation parallelism with shuffle partitions.

**Parameters:**
- `master` (string): Spark master URL (e.g., local[4], k8s://https://cluster:6443)
- `packages` (string): Maven coordinates for Kafka connector
- `shuffle_partitions` (integer): Number of shuffle partitions for aggregation

**Commands:**
- `spark-submit --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 streaming.py`
- `spark-submit --deploy-mode cluster --master k8s://https://cluster:6443 --class com.app.StreamJob app.jar`
- `spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1`
- `spark-submit --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 --conf spark.sql.shuffle.partitions=200 streaming.py`
- `kafka-console-producer --broker-list localhost:9092 --topic events`

**Examples:**
- spark-submit --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 streaming.py
- spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1
- kafka-console-producer --broker-list localhost:9092 --topic events

## References
- [Spark Kafka integration guide](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)