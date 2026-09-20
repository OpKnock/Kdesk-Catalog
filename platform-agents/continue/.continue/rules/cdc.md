---
name: "Cdc"
description: "Implement Change Data Capture with Debezium and Kafka Connect: connectors, topics, and consuming change events."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

# Cdc

Implement Change Data Capture with Debezium and Kafka Connect: connectors, topics, and consuming change events.

## Instructions

# Change Data Capture (CDC)

Stream database changes to Kafka with Debezium and Kafka Connect.

## When to Use

- Feeding search indexes, caches, or analytics from database writes
- Building event-driven pipelines from existing relational data
- Replicating changes without application code changes

## Deploy Debezium Connect

```bash
docker run -d --name connect -p 8083:8083 quay.io/debezium/connect:latest
curl http://localhost:8083/connectors
```

## Register a Connector

```json
{
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname": "appdb",
    "database.server.name": "dbserver",
    "table.include.list": "public.users",
    "plugin.name": "pgoutput"
  }
}
```

```bash
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @debezium.json
curl -s http://localhost:8083/connectors/postgres-connector/status | jq '.connector.state'
```

## Consume Events

```bash
kafka-topics --bootstrap-server localhost:9092 --list | grep dbserver
kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning
```

Each record has op (c/u/d), before, after, and source metadata.

## Testing

```bash
# Insert a row and watch the event
psql -c "INSERT INTO users (name) VALUES ('alice');"
kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning --max-messages 1
```

## Best Practices

- Use logical decoding (pgoutput) for Postgres
- Include table.include.list to limit capture
- Handle schema changes with Debezium schema evolution
- Set IDs and keys on events for exactly-once consumers
- Monitor connector status in production

## Capabilities

### debezium-connect
Deploy Debezium Connect and register source connectors via the Kafka Connect REST API

**Commands:**
- `docker run -d --name connect -p 8083:8083 quay.io/debezium/connect:latest`
- `curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @debezium.json`
- `curl http://localhost:8083/connectors`
- `curl -X DELETE http://localhost:8083/connectors/postgres-connector`

**Examples:**
- curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @debezium.json
- curl -s http://localhost:8083/connectors | jq '.connectors'
- curl -s http://localhost:8083/connectors/postgres-connector/status | jq '.connector.state'

### kafka-streams
Inspect CDC topics and consume change events from Kafka

**Commands:**
- `kafka-topics --bootstrap-server localhost:9092 --list`
- `kafka-topics --bootstrap-server localhost:9092 --describe --topic dbserver.public.users`
- `kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning`
- `kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning --property print.key=true --property key.separator=--`

**Examples:**
- kafka-topics --bootstrap-server localhost:9092 --list | grep dbserver
- kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning | jq '.payload.op'
- kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning --max-messages 5