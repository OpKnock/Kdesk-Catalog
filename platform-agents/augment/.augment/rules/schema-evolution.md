---
type: agent_requested
description: "Expert reference covering Avro compatibility modes, protoc descriptor generation, and backward/forward compatibility checks for streaming contracts. Use when working with schema compat, api or when the user mentions schema compat, api."
---

Expert reference covering Avro compatibility modes, protoc descriptor generation, and backward/forward compatibility checks for streaming contracts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `java -jar avro-tools-1.11.3.jar getschema user.avsc`
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