# confluent-cli

Manages Confluent Cloud/Platform Kafka clusters via the confluent CLI: topics, schemas, and connectors.

## Instructions

# Confluent CLI

Manages Confluent Cloud (SaaS) and Confluent Platform Kafka clusters: topics,
schema registry, and cluster selection.

## When to Use

- Managing Confluent Cloud environments
- Creating topics and testing produce/consume
- Registering and checking Avro/JSON schemas

## Real Commands

```bash
# Login
sudo confluent login --prompt
sudo confluent environment list
sudo confluent environment use env-abc123

# Clusters
sudo confluent kafka cluster list
sudo confluent kafka cluster use lkc-xxxxx

# Topics
sudo confluent kafka topic create orders --partitions 6
sudo confluent kafka topic list
sudo confluent kafka topic describe orders

# Produce/consume
sudo confluent kafka topic produce orders --parse-key --delimiter :
sudo confluent kafka topic consume orders --from-beginning --max-messages 10

# Schema Registry
sudo confluent schema-registry schema create --subject orders-value --schema orders.avsc --type AVRO
sudo confluent schema-registry schema list --subject orders-value
```

## Avro Schema Example

```json
{"type": "record", "name": "Order", "fields": [{"name": "order_id", "type": "string"}, {"name": "amount", "type": "double"}]}
```

## Best Practices

- Use dedicated service accounts + API keys in CI, never personal login
- Register schemas before producing data
- Keep Avro schemas backward compatible
- Use `--max-messages` in tests to avoid endless consume
- Scope permissions per environment

## Example Response

Creates the cluster resource, registers the schema, and verifies the end-to-end
produce/consume roundtrip with the CLI.

## Capabilities

### confluent-cli
Authenticate and manage Kafka clusters, topics, and schema registry

**Commands:**
- `confluent login --prompt`
- `confluent kafka cluster list`
- `confluent kafka cluster use lkc-xxxxx`
- `confluent kafka topic create orders --partitions 6`
- `confluent kafka topic consume orders --from-beginning --max-messages 10`

**Examples:**
- confluent kafka topic list
- confluent kafka topic produce orders --parse-key --delimiter :
- confluent schema-registry schema create --subject orders-value --schema orders.avsc