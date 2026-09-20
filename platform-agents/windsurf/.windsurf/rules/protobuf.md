---
trigger: glob
description: "Protocol Buffers: proto authoring, protoc code generation, buf lint/breaking checks, and gRPC schema workflows."
globs: ["**/*.go", "**/*.java", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Protobuf

Protocol Buffers: proto authoring, protoc code generation, buf lint/breaking checks, and gRPC schema workflows.

## Instructions

# Protocol Buffers

Protobuf is a compact, language-neutral schema-driven serialization format.

## What this skill does

- Authors .proto schemas
- Generates code with protoc or buf
- Enforces compatibility with breaking checks

## When to use

- gRPC services
- Binary payloads shared across languages

## Real commands

```bash
# Compile for Go (needs protoc-gen-go)
protoc --go_out=. --go_opt=paths=source_relative user.proto
protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. user.proto

# Java / Python
protoc --java_out=. user.proto
protoc --python_out=. user.proto

# buf workflow
buf lint
buf generate
buf breaking --against .git#branch=main
```

## proto example

```proto
syntax = "proto3";

message User {
  string id = 1;
  string name = 2;
  repeated string roles = 3;
}
```

## Compatibility rules

- Never change field numbers
- Adding fields is safe; removing is breaking
- Use reserved for retired fields

## Best practices

- Run buf breaking in CI before merging
- One package per domain; keep files small
- Use buf.gen.yaml to standardize generation

## Capabilities

### protobuf-generation
Compile .proto files to Go/Java/Python, lint with buf, and check breaking changes.

**Commands:**
- `protoc --version`
- `protoc --go_out=. --go_opt=paths=source_relative user.proto`
- `protoc --java_out=. user.proto`
- `protoc --python_out=. user.proto`
- `buf lint`

**Examples:**
- protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. user.proto
- buf generate
- buf breaking --against .git#branch=main
