---
type: agent_requested
description: "Implement Change Data Capture with Debezium and Kafka Connect: connectors, topics, and consuming change events. Use when working with debezium connect, kafka streams, api or when the user mentions debezium connect, kafka streams, api."
---

Implement Change Data Capture with Debezium and Kafka Connect: connectors, topics, and consuming change events.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d --name connect -p 8083:8083 quay.io/debezium/c`, `kafka-topics --bootstrap-server localhost:9092 --list`
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

**Parameters:**
- `connector_name` (string): Name of the Debezium connector
- `connector_config` (string): JSON config file for the connector

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

**Parameters:**
- `topic` (string): Kafka topic name, e.g. dbserver.public.users
- `bootstrap_servers` (string): Kafka bootstrap servers, e.g. localhost:9092

**Commands:**
- `kafka-topics --bootstrap-server localhost:9092 --list`
- `kafka-topics --bootstrap-server localhost:9092 --describe --topic dbserver.public.users`
- `kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning`
- `kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning --property print.key=true --property key.separator=--`

**Examples:**
- kafka-topics --bootstrap-server localhost:9092 --list | grep dbserver
- kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning | jq '.payload.op'
- kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver.public.users --from-beginning --max-messages 5

## References
- [Debezium Documentation](https://debezium.io/documentation/reference/stable/index.html)
- [Kafka Connect API](https://kafka.apache.org/documentation/#connect_rest)