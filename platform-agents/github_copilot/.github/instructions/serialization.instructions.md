---
applyTo: "**/*.go **/*.json **/*.py **/*.r **/*.rs **/*.sh **/*.{ts,tsx}"
---

Generates typed code from Protocol Buffers and FlatBuffers schemas, validates and pretty-prints JSON payloads, and compares wire formats for size and schema evolution fit. Supports Go, Python, TypeScript, and Rust code generation pipelines.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `protoc --version`
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

# Serialization

Hand-crafted skill for choosing and operating serialization formats.

## What this skill does

- Generates typed code from protobuf and flatbuffers schemas
- Validates and pretty-prints JSON payloads
- Compares formats for size and schema evolution fit

## When to use

- Picking a wire format for a new service-to-service contract
- Regenerating code after a schema change
- Debugging malformed JSON in API logs

## Real commands

```bash
# Protobuf codegen
protoc --version
protoc --python_out=. --proto_path=. user.proto
protoc --go_out=. --go_opt=paths=source_relative user.proto

# FlatBuffers
flatc --ts user.fbs

# JSON tooling
python -m json.tool payload.json
jq -c '.items[] | select(.price > 10)' data.json
jq '.data | keys' response.json
```

## Schema example

```proto
syntax = "proto3";
message User {
  string id = 1;
  string email = 2;
  int64 created_at = 3;
}
```

```fbs
namespace app;
table User {
  id: string;
  email: string;
}
root_type User;
```

## Testing

```bash
protoc --python_out=. --proto_path=. user.proto && python -c 'import user_pb2; print(user_pb2.User(id="1", email="a@b.c"))'
python -m json.tool payload.json > /dev/null && echo valid
```

## Best practices

- Protobuf for high-traffic RPC payloads; JSON for external APIs
- Keep field numbers stable; they are the wire contract
- Validate JSON with jq or json.tool before it reaches consumers

## Capabilities

### serialization-toolchain
Compile and inspect serialization schemas and payloads

**Parameters:**
- `schema_file` (string): Input .proto or .fbs schema
- `language` (string): Target language for code generation
- `input_file` (string): Data file to validate or pretty-print

**Commands:**
- `protoc --version`
- `protoc --python_out=. --proto_path=. user.proto`
- `flatc --ts user.fbs`
- `python -m json.tool payload.json`
- `jq -c '.items[] | select(.price > 10)' data.json`

**Examples:**
- protoc --go_out=. --go_opt=paths=source_relative user.proto
- flatc --ts user.fbs
- python -m json.tool payload.json

## References
- [Protocol Buffers Documentation](https://protobuf.dev/)
- [FlatBuffers Documentation](https://flatbuffers.dev/)
- [jq Manual](https://jqlang.github.io/jq/manual/)
