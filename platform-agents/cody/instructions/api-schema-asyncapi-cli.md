# Api Schema Asyncapi Cli

Authors event API schemas with AsyncAPI and Apache Avro: AsyncAPI document validation and generation, Avro schema tooling, and Kafka payload contracts.

## Instructions

# API Schema v4 - AsyncAPI/Avro

Event schema authoring.

## What This Skill Does
- Documents event-driven APIs with AsyncAPI
- Compiles Avro schemas for Kafka
- Generates docs and stubs

## When to Use
- Kafka/Kinesis event contracts
- Event-driven microservices
- Schema registry management

## Real Commands

```bash
npm install -g @asyncapi/cli
asyncapi validate asyncapi.yaml
asyncapi generate fromTemplate asyncapi.yaml @asyncapi/html-template -o docs
java -jar avro-tools-1.11.3.jar compile schema user.avsc .
```

## Avro Schema

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    { "name": "id", "type": "long" },
    { "name": "email", "type": "string" }
  ]
}
```

## Testing
- Validate documents in CI
- Round-trip JSON to Avro and back
- Check schema registry compatibility

## Best Practices
- Version event schemas with a registry
- Use forward/backward compatible fields
- Keep AsyncAPI docs in sync with topics

## Capabilities

### asyncapi-cli
Validate and generate AsyncAPI documents

**Commands:**
- `npm install -g @asyncapi/cli`
- `asyncapi validate asyncapi.yaml`
- `asyncapi new --example=tutorial`
- `asyncapi generate fromTemplate asyncapi.yaml @asyncapi/html-template -o docs`
- `asyncapi bundle asyncapi.yaml -o bundled.yaml`

**Examples:**
- asyncapi validate checks document structure
- asyncapi new scaffolds an example
- generate fromTemplate builds HTML docs

### avro-tools
Compile and inspect Avro schemas

**Commands:**
- `java -jar avro-tools-1.11.3.jar compile schema user.avsc .`
- `java -jar avro-tools-1.11.3.jar getmeta user.avsc`
- `java -jar avro-tools-1.11.3.jar tojson users.avro`
- `java -jar avro-tools-1.11.3.jar fromjson --schema-file user.avsc users.json > users.avro`
