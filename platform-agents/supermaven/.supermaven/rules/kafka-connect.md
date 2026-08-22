# Kafka Connect

Run and operate Kafka Connect clusters: standalone and distributed workers, connector lifecycle via the REST API, and status/offset inspection.

## Instructions

# Kafka Connect

Run and manage Kafka Connect for streaming data between Kafka and external systems.

## What this skill does

- Starts standalone and distributed Connect workers.
- Creates, lists, pauses, and deletes connectors via the REST API.
- Inspects task status, configs, and offset topics.

## When to use

- Ingesting DB/file/S3 data into Kafka (source connectors).
- Sinking Kafka data to Elasticsearch, S3, or JDBC (sink connectors).
- CDC pipelines with Debezium.

## Real commands

```bash
# Distributed worker
connect-distributed.sh config/connect-distributed.properties

# Standalone (dev) with one source connector
connect-standalone.sh config/connect-standalone.properties \
  config/connector-file-source.properties

# List connectors
curl -s http://localhost:8083/connectors

# Create a connector from JSON
curl -s -X POST http://localhost:8083/connectors \
  -H 'Content-Type: application/json' -d @file-source.json

# Check status (task assignment, errors)
curl -s http://localhost:8083/connectors/file-source/status | jq .

# List installed connector plugins
curl -s http://localhost:8083/connector-plugins | jq '.[].class'

# Delete a connector
curl -s -X DELETE http://localhost:8083/connectors/file-source
```

## Connector JSON example

```json
{
  "name": "file-source",
  "config": {
    "connector.class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "tasks.max": "1",
    "topic": "orders",
    "file": "/data/orders.log"
  }
}
```

## Testing

```bash
# Verify offsets topic exists in distributed mode
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic connect-offsets
```

## Best practices

- Use distributed mode in production for rebalancing and failover.
- Name connectors <source|sink>-<system>-<name>; one connector per logical pipeline.
- Monitor /connectors/<name>/status in your alerting; tasks fail fast on bad schemas.

## Capabilities

### worker-runtime
Start Kafka Connect in standalone or distributed mode.

**Commands:**
- `connect-distributed.sh config/connect-distributed.properties`
- `connect-standalone.sh config/connect-standalone.properties config/connector-file-source.properties`
- `connect-distributed.sh config/connect-distributed.properties config/worker-log4j.properties`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic connect-offsets`

**Examples:**
- connect-distributed.sh config/connect-distributed.properties
- connect-standalone.sh config/connect-standalone.properties config/connector-file-source.properties
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic connect-offsets

### connector-rest
Manage connectors through the Connect REST API (port 8083 by default).

**Commands:**
- `curl -s http://localhost:8083/connectors`
- `curl -s -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d @file-source.json`
- `curl -s http://localhost:8083/connectors/file-source/status`
- `curl -s http://localhost:8083/connector-plugins`
- `curl -s -X DELETE http://localhost:8083/connectors/file-source`

**Examples:**
- curl -s -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d @file-source.json
- curl -s http://localhost:8083/connectors/file-source/status | jq .tasks
- curl -s http://localhost:8083/connector-plugins | jq '.[].class'