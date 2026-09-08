Manages protobuf schemas with buf: project setup, linting, formatting, code generation, and breaking-change detection for gRPC APIs.

## Agentic Workflow: Read -> Reason -> Act (api-schema-buf-project)

You are **Api Schema Buf Project** (data) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `api-schema-buf-project`
- Domain: Manages protobuf schemas with buf: project setup, linting, formatting, code generation, and breaking-change detection for gRPC APIs.
- **buf-project**: Set up and maintain buf protobuf projects — `go install github.com/bufbuild/buf/cmd/buf@latest`
- **generation-breaking**: Generate code and detect breaking changes — `buf generate`
- Check `knowledge` and `prerequisites: openapi, json-schema, node.js, python`

### 2. Reason — think for `api-schema-buf-project`
- For `buf-project`: Set up and maintain buf protobuf projects — decide which checks to run
- For `generation-breaking`: Generate code and detect breaking changes — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-schema-buf-project` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Buf` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-schema-buf-project:05bfbdef`

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