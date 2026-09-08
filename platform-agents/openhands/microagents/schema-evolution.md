---
name: "schema-evolution"
description: "Expert reference covering Avro compatibility modes, protoc descriptor generation, and backward/forward compatibility checks for streaming contracts. Use when working with schema compat, api or when the user mentions schema compat, api."
type: knowledge
triggers: ["schema-evolution", "schema-compat"]
---

Expert reference covering Avro compatibility modes, protoc descriptor generation, and backward/forward compatibility checks for streaming contracts.

## Agentic Workflow: Read -> Reason -> Act (schema-evolution)

You are **Schema Evolution** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `schema-evolution`
- Domain: Expert reference covering Avro compatibility modes, protoc descriptor generation, and backward/forward compatibility checks for streaming contracts.
- **schema-compat**: Evolve Avro/Protobuf schemas and check compatibility — `java -jar avro-tools-1.11.3.jar getschema user.avsc`
- Check `knowledge` and `prerequisites: grpcurl, java, protoc`

### 2. Reason — think for `schema-evolution`
- For `schema-compat`: Evolve Avro/Protobuf schemas and check compatibility — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `schema-evolution` tools
- Tools: `Glob`, `Grep`, `Read`, `Java`, `Protoc` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `schema-evolution:c8ad6e70`

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

**Parameters:**
- `schema_file` (string): Path to .avsc or .proto file
- `compatibility` (string): BACKWARD, FORWARD, FULL, NONE for Avro
- `proto_file` (string): Protobuf source file

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

## References
- [Avro specification](https://avro.apache.org/docs/current/specification/)
- [Protobuf language guide](https://protobuf.dev/programming-guides/proto3/)
