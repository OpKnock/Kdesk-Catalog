---
trigger: glob
description: "Generates typed code from Protocol Buffers and FlatBuffers schemas, validates and pretty-prints JSON payloads, and compares wire formats for size and schema evolution fit. Supports Go, Python, TypeScript, and Rust code generation pipelines."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{ts,tsx}"]
---

# Serialization

Generates typed code from Protocol Buffers and FlatBuffers schemas, validates and pretty-prints JSON payloads, and compares wire formats for size and schema evolution fit. Supports Go, Python, TypeScript, and Rust code generation pipelines.

## Instructions

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
