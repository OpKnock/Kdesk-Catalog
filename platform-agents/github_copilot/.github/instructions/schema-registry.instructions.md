---
applyTo: "**/*.json **/*.r **/*.sh"
---

# Schema Registry

Expert Confluent Schema Registry reference covering Avro schema registration, compatibility checking before promotion, and subject/version listing via REST.

## Instructions

# Schema Registry

Expert skill for managing Avro schemas with Confluent Schema Registry.

## What this skill does

- Lists subjects and versions registered in the registry
- Registers new schema versions over the REST API
- Pre-checks compatibility before a schema can break consumers

## When to use

- Releasing a new Kafka message format
- Enforcing backward compatibility on shared topics
- Investigating schema-not-found producer errors

## Real commands

```bash
# List subjects
curl -s http://localhost:8081/subjects

# Latest version of one subject
curl -s http://localhost:8081/subjects/orders-value/versions/latest | jq .version

# Register a new version (payload: {"schema": "..."})
curl -X POST http://localhost:8081/subjects/orders-value/versions -H 'Content-Type: application/vnd.schemaregistry.v1+json' -d @new-schema.json

# Compatibility check against latest (BACKWARD by default)
curl -s -H 'Content-Type: application/vnd.schemaregistry.v1+json' 'http://localhost:8081/compat/subjects/orders-value/versions/latest' -d @candidate.json

# Produce with the registry
kafka-avro-console-producer --broker-list localhost:9092 --topic orders --property schema.registry.url=http://localhost:8081 --property value.schema="$(cat order.avsc)"
```

## Config

```json
// candidate.json
{ "schema": "{"type":"record","name":"Order","fields":[{"name":"id","type":"long"},{"name":"email","type":"string","default":""}]}" }
```

## Testing

```bash
curl -s http://localhost:8081/subjects/orders-value/versions | jq
curl -s http://localhost:8081/config | jq   # current compatibility mode
```

## Best practices

- Set compatibility per subject before the first breaking need: BACKWARD
- Check /compat before registering, not after producers fail
- Version consumers with the same tag as the schema version

## Capabilities

### schema-registry-api
Register and validate schemas against the Confluent Schema Registry

**Commands:**
- `curl -s http://localhost:8081/subjects`
- `curl -s http://localhost:8081/subjects/orders-value/versions/latest | jq .version`
- `curl -X POST http://localhost:8081/subjects/orders-value/versions -H 'Content-Type: application/vnd.schemaregistry.v1+json' -d @new-schema.json`
- `curl -s -H 'Content-Type: application/vnd.schemaregistry.v1+json' 'http://localhost:8081/compat/subjects/orders-value/versions/latest' -d @candidate.json`
- `kafka-avro-console-producer --broker-list localhost:9092 --topic orders --property schema.registry.url=http://localhost:8081 --property value.schema="$(cat order.avsc)"`

**Examples:**
- curl -s http://localhost:8081/subjects/orders-value/versions | jq
- curl -X POST http://localhost:8081/subjects/orders-value/versions -H 'Content-Type: application/vnd.schemaregistry.v1+json' -d @new-schema.json
- curl -s http://localhost:8081/config | jq
