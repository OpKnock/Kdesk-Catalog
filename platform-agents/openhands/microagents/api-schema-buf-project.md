---
name: "api-schema-buf-project"
description: "Manages protobuf schemas with buf: project setup, linting, formatting, code generation, and breaking-change detection for gRPC APIs."
type: knowledge
triggers: ["api-schema-buf-project", "buf-project", "generation-breaking"]
---

# Api Schema Buf Project

Manages protobuf schemas with buf: project setup, linting, formatting, code generation, and breaking-change detection for gRPC APIs.

## Instructions

# API Schema v3 - Protobuf/buf

Protobuf schema management with buf.

## What This Skill Does
- Manages proto schemas as buf modules
- Lints and formats proto files
- Generates stubs and checks compatibility

## When to Use
- gRPC API schema management
- Multi-language stub generation
- Safe schema evolution

## Real Commands

```bash
go install github.com/bufbuild/buf/cmd/buf@latest
buf mod init
buf lint
buf format -w
buf generate
buf breaking --against .git#branch=main
```

## Example proto

```proto
syntax = "proto3";
package api.v1;

message User {
  int64 id = 1;
  string email = 2;
}
```

## Testing
- Run buf lint and breaking checks in CI
- Generate stubs into a scratch dir
- Test wire compatibility after changes

## Best Practices
- Never reuse field numbers
- Add fields at the end of messages
- Commit generated code for release tags

## Capabilities

### buf-project
Set up and maintain buf protobuf projects

**Commands:**
- `go install github.com/bufbuild/buf/cmd/buf@latest`
- `buf --version`
- `buf mod init`
- `buf lint`
- `buf format -w`

**Examples:**
- buf mod init creates buf.yaml
- buf lint checks proto style rules
- buf format -w normalizes formatting

### generation-breaking
Generate code and detect breaking changes

**Commands:**
- `buf generate`
- `buf generate --template buf.gen.yaml`
- `buf breaking --against .git#branch=main`
- `buf build -o schema.binpb`

**Examples:**
- -cli --help
- -api --help
