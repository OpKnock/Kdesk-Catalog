---
name: "Schema Evolution"
description: "Expert reference covering Avro compatibility modes, protoc descriptor generation, and backward/forward compatibility checks for streaming contracts."
globs: ["**/*.java", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Schema Evolution

Expert reference covering Avro compatibility modes, protoc descriptor generation, and backward/forward compatibility checks for streaming contracts.

## Instructions

# Schema Evolution

Expert skill for evolving serialization schemas without breaking consumers.

## What this skill does

- Compiles Avro and Protobuf schemas to check they parse
- Generates descriptors to inspect wire contracts
- Applies compatibility rules so old and new readers interoperate

## When to use

- Adding fields to a schema consumed by old versions
- Migrating a topic's message format
- Reviewing a schema PR for breaking changes

## Real commands

```bash
# Parse and validate an Avro schema
java -jar avro-tools-1.11.3.jar getschema user.avsc

# Generate Java/Python classes
java -jar avro-tools-1.11.3.jar compile schema user.avsc out/

# Protobuf toolchain
protoc --version
protoc --descriptor_set_out=user.pb --include_imports user.proto

# Inspect a compiled service descriptor
grpcurl -protoset user.pb list
```

## Avro compatibility rules

- BACKWARD: new schema can read old data (add fields with defaults)
- FORWARD: old schema can read new data (remove-only safe)
- FULL: both directions
- Adding a required field is a breaking change without a default

## Protobuf rules

- Never reuse a field number with a different type
- Add fields with new numbers; old clients ignore them
- Renaming a field keeps the number, so wire compatibility holds

## Testing

```bash
java -jar avro-tools-1.11.3.jar getschema user.avsc
protoc --descriptor_set_out=user.pb --include_imports user.proto && grpcurl -protoset user.pb list
```

## Best practices

- Give new fields defaults when the consumer may be older
- Register schemas in the schema registry before deploying producers
- Treat any schema change as a release note for consumers

## Capabilities

### schema-compat
Evolve Avro/Protobuf schemas and check compatibility

**Commands:**
- `java -jar avro-tools-1.11.3.jar getschema user.avsc`
- `java -jar avro-tools-1.11.3.jar compile schema user.avsc .`
- `protoc --version`
- `protoc --descriptor_set_out=user.pb --include_imports user.proto`
- `grpcurl -protoset user.pb list`

**Examples:**
- java -jar avro-tools-1.11.3.jar compile schema user.avsc out/
- protoc --descriptor_set_out=user.pb --include_imports user.proto
- java -jar avro-tools-1.11.3.jar getmeta user.avsc