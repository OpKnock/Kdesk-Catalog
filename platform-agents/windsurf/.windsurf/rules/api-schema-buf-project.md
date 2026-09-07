---
trigger: glob
description: "Manages protobuf schemas with buf: project setup, linting, formatting, code generation, and breaking-change detection for gRPC APIs. Use when working with buf project, generation breaking or when the user mentions buf project, generation breaking."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Manages protobuf schemas with buf: project setup, linting, formatting, code generation, and breaking-change detection for gRPC APIs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go install github.com/bufbuild/buf/cmd/buf@latest`, `buf generate`
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

**Parameters:**
- `module` (string): Buf module path
- `input` (string): Input directory or file
- `against` (string): Baseline for breaking checks

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

## References
- [buf Docs](https://buf.build/docs/)
- [Protobuf Language Guide](https://protobuf.dev/programming-guides/proto3/)
