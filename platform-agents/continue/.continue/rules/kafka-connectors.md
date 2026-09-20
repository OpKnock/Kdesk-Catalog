---
name: "Kafka Connectors"
description: "Deploy specific Kafka connectors: Debezium CDC sources, JDBC, and S3 sinks, including plugin installation with confluent-hub and change-data streaming."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

# Kafka Connectors

Deploy specific Kafka connectors: Debezium CDC sources, JDBC, and S3 sinks, including plugin installation with confluent-hub and change-data streaming.

## Instructions

# Kafka Connectors (Specific)

Deploy real connector plugins: Debezium CDC sources and common sinks.

## What this skill does

- Installs connector plugins with confluent-hub.
- Creates Debezium CDC connectors for databases.
- Monitors CDC topics and connector task state.

## When to use

- Streaming database changes to downstream systems (CDC).
- Sinking Kafka data to JDBC stores or S3 lakes.
- Auditing which connector classes are available on a worker.

## Real commands

```bash
# Install Debezium MySQL connector
confluent-hub install debezium/debezium-connector-mysql:2.5.0 \
  --component-dir /opt/connect-plugins --no-prompt

# Install JDBC and S3 connectors
confluent-hub install confluentinc/kafka-connect-jdbc:latest --no-prompt
confluent-hub install confluentinc/kafka-connect-s3:latest --no-prompt

# Restart worker to load new plugins
systemctl restart kafka-connect

# Verify plugin is visible
curl -s http://localhost:8083/connector-plugins | jq -r '.[].class' | grep -i debezium

# Create Debezium MySQL source
curl -s -X POST http://localhost:8083/connectors \
  -H 'Content-Type: application/json' -d @debezium-mysql.json

# Watch change events
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic dbserver.mydb.products --from-beginning

# Pause/resume to stop data flow temporarily
curl -s -X PUT http://localhost:8083/connectors/debezium-mysql/pause
curl -s -X PUT http://localhost:8083/connectors/debezium-mysql/resume
```

## Debezium config example

```json
{
  "name": "debezium-mysql",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "db-01",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "secret",
    "database.server.name": "dbserver",
    "database.include.list": "mydb",
    "table.include.list": "mydb.products",
    "database.history.kafka.bootstrap.servers": "localhost:9092",
    "database.history.kafka.topic": "schema-changes.dbserver",
    "include.schema.changes": "true"
  }
}
```

## Testing

```bash
# A row update in MySQL should appear as a JSON change event in the topic
mysql -h db-01 -u debezium -p mydb -e "UPDATE products SET price=9.99 WHERE id=1"
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic dbserver.mydb.products --from-beginning
```

## Best practices

- Pin connector versions; never use :latest in production.
- Give Debezium its own DB user with minimal grants (SELECT, RELOAD, SHOW DATABASES).
- Watch task states; failed CDC tasks silently stall downstream data.

## Capabilities

### plugin-install
Install connector plugins into the Connect worker with confluent-hub.

**Commands:**
- `confluent-hub install debezium/debezium-connector-mysql:2.5.0 --component-dir /opt/connect-plugins`
- `confluent-hub install confluentinc/kafka-connect-jdbc:latest --no-prompt`
- `confluent-hub install confluentinc/kafka-connect-s3:latest --no-prompt`
- `curl -s http://localhost:8083/connector-plugins | jq -r '.[].class' | grep -i debezium`

**Examples:**
- confluent-hub install debezium/debezium-connector-mysql:2.5.0 --component-dir /opt/connect-plugins --no-prompt
- confluent-hub install confluentinc/kafka-connect-jdbc:latest --no-prompt
- curl -s http://localhost:8083/connector-plugins | jq -r '.[].class' | grep -i jdbc

### cdc-pipeline
Create and monitor a Debezium CDC connector capturing database changes.

**Commands:**
- `curl -s -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d @debezium-mysql.json`
- `curl -s http://localhost:8083/connectors/debezium-mysql/status | jq '.connector,.tasks'`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic dbserver.mydb.products --from-beginning`
- `curl -s -X PUT http://localhost:8083/connectors/debezium-mysql/pause`
- `curl -s http://localhost:8083/connectors/debezium-mysql/tasks/0/topics`

**Examples:**
- curl -s -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d @debezium-mysql.json
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic dbserver.mydb.products --from-beginning
- curl -s http://localhost:8083/connectors/debezium-mysql/status | jq '.tasks[0].state'