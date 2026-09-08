---
name: "protobuf"
description: "Protocol Buffers: proto authoring, protoc code generation, buf lint/breaking checks, and gRPC schema workflows. Use when working with protobuf generation, api or when the user mentions protobuf generation, api."
license: "MIT"
compatibility: "Requires buf, protoc."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(buf:*) Bash(protoc:*)"
---

Protocol Buffers: proto authoring, protoc code generation, buf lint/breaking checks, and gRPC schema workflows.

## Agentic Workflow: Read -> Reason -> Act (protobuf)

You are **Protobuf** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `protobuf`
- Domain: Protocol Buffers: proto authoring, protoc code generation, buf lint/breaking checks, and gRPC schema workflows.
- **protobuf-generation**: Compile .proto files to Go/Java/Python, lint with buf, and check breaking changes. — `protoc --version`
- Check `knowledge` and `prerequisites: buf, protoc`

### 2. Reason — think for `protobuf`
- For `protobuf-generation`: Compile .proto files to Go/Java/Python, lint with buf, and check breaking changes. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `protobuf` tools
- Tools: `Glob`, `Grep`, `Read`, `Protoc`, `Buf` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `protobuf:7716a476`

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

**Parameters:**
- `proto_file` (string): Path to the .proto file
- `language` (string): go, java, python, cpp, etc.
- `out_dir` (string): Output directory for generated code

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

## References
- [Protobuf.dev](https://protobuf.dev/)
- [Buf Docs](https://buf.build/docs/)
