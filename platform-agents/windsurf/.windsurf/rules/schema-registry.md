---
trigger: glob
description: "Expert Confluent Schema Registry reference covering Avro schema registration, compatibility checking before promotion, and subject/version listing via REST. Use when working with schema registry api or when the user mentions schema registry api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Expert Confluent Schema Registry reference covering Avro schema registration, compatibility checking before promotion, and subject/version listing via REST.

## Agentic Workflow: Read -> Reason -> Act (schema-registry)

You are **Schema Registry** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `schema-registry`
- Domain: Expert Confluent Schema Registry reference covering Avro schema registration, compatibility checking before promotion, and subject/version listing via REST.
- **schema-registry-api**: Register and validate schemas against the Confluent Schema Registry — `curl -s http://localhost:8081/subjects`
- Check `knowledge` and `prerequisites: kafka-avro-console-producer`

### 2. Reason — think for `schema-registry`
- For `schema-registry-api`: Register and validate schemas against the Confluent Schema Registry — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `schema-registry` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Kafka-avro-console-producer` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `schema-registry:4e623359`

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

**Parameters:**
- `subject` (string): Subject name, e.g. orders-value
- `schema_file` (string): JSON file with {"schema": "..."} payload
- `registry_url` (string): Schema Registry base URL

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

## References
- [Schema Registry API reference](https://docs.confluent.io/platform/current/schema-registry/develop/api.html)
- [Schema Registry docs](https://docs.confluent.io/platform/current/schema-registry/index.html)
