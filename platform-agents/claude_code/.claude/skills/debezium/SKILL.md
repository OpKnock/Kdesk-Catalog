---
name: "debezium"
description: "Registers, inspects, and troubleshoots Kafka Connect connectors that stream row-level changes from MySQL, PostgreSQL, and MongoDB via Debezium CDC. Use when working with connector management, api or when the user mentions connector management, api."
license: "MIT"
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*)"
---

Registers, inspects, and troubleshoots Kafka Connect connectors that stream row-level changes from MySQL, PostgreSQL, and MongoDB via Debezium CDC.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST http://localhost:8083/connectors -H 'Content-Ty`
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

# Debezium

## What this skill does

Debezium is a CDC platform built on Kafka Connect that captures row-level changes from databases and publishes them as events to Kafka. This skill covers connector registration, status inspection, task restart, and snapshot handling.

## When to use

- Streaming database changes into Kafka for event-driven systems
- Building change-data pipelines (audit, search indexing, cache invalidation)
- Investigating connectors stuck in FAILED or UNASSIGNED state

## Real commands

```bash
# Register a connector from a JSON config file
curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d @mysql-source.json

# List all connectors and their status
curl -s http://localhost:8083/connectors | jq
curl -s http://localhost:8083/connectors/mysql-source/status | jq '.connector.state, .tasks'

# Restart a failed task
curl -X POST http://localhost:8083/connectors/mysql-source/tasks/0/restart

# Remove a connector and its Kafka topics are kept
curl -X DELETE http://localhost:8083/connectors/mysql-source
```

## Connector configuration example

```json
{
  "name": "mysql-source",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "db.internal",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "secret",
    "database.server.id": "5400",
    "database.include.list": "orders",
    "topic.prefix": "cdc"
  }
}
```

## Testing

```bash
# Verify the connector picked up and read the binlog
kafka-console-consumer --bootstrap-server localhost:9092 --topic cdc.orders.orders --from-beginning

# Trigger a snapshot rerun without losing the offsets
curl -X POST http://localhost:8083/connectors/mysql-source/stop

```

## Best practices

- Use a dedicated DB user with only SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, and REPLICATION CLIENT privileges for MySQL.
- Give each connector a unique `database.server.id` to avoid master/slave id conflicts.
- Monitor `binlog` retention on the source DB; Debezium cannot catch up once the binlog position is purged.
- Prefer `snapshot.mode: when_needed` or incremental snapshots for large tables.
- Use offset storage topics with enough partitions and a sane retention.

## Capabilities

### connector-management
Register, list, inspect status, and restart Debezium Kafka Connect connectors via the Connect REST API.

**Parameters:**
- `connector-name` (string): Name of the connector to inspect or restart (e.g. mysql-source)
- `connect-url` (string): Kafka Connect REST endpoint, default http://localhost:8083
- `task-id` (integer): Zero-based index of the failing task to restart

**Commands:**
- `curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d @mysql-source.json`
- `curl -s http://localhost:8083/connectors | jq`
- `curl -s http://localhost:8083/connectors/mysql-source/status | jq '.connector.state, .tasks'`
- `curl -X POST http://localhost:8083/connectors/mysql-source/tasks/0/restart`
- `curl -X DELETE http://localhost:8083/connectors/mysql-source`

**Examples:**
- curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d @mysql-source.json
- curl -s http://localhost:8083/connectors/mysql-source/status | jq '.connector.state, .tasks'
- curl -s http://localhost:8083/connectors/mysql-source/config | jq

## References
- [Debezium Documentation](https://debezium.io/documentation/reference/stable/index.html)
