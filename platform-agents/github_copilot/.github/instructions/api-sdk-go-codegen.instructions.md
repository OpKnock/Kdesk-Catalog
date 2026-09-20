---
applyTo: "**/*.go **/*.r **/*.sh **/*.{yaml,yml}"
---

Generates Go SDKs with oapi-codegen: typed clients from OpenAPI, server stubs, config generation, and go test verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-`, `go test ./...`
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

# API SDK v4 - Go

Go SDK generation with oapi-codegen.

## What This Skill Does
- Generates typed Go clients and servers
- Configures generation via YAML
- Validates with go build and tests

## When to Use
- Go services consuming the API
- Generating server stubs for parity
- Typed client SDKs

## Real Commands

```bash
go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest
oapi-codegen -package api -generate types,client -o client.gen.go openapi.yaml
go build ./...
go test ./...
```

## Config File

```yaml
package: api
output: gen/client.gen.go
generate:
  client: true
  models: true
  chi-server: true
```

## Testing
- Compile after regeneration
- Test client calls with httptest servers
- Run go vet in CI

## Best Practices
- Commit generated files with release tags
- Keep generation config in the repo
- Regenerate before each release

## Capabilities

### go-codegen
Generate Go client code from OpenAPI

**Parameters:**
- `package` (string): Go package name
- `generate` (string): Comma-separated generation targets
- `output` (string): Output Go file

**Commands:**
- `go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest`
- `oapi-codegen -package api -generate types,client -o client.gen.go openapi.yaml`
- `oapi-codegen -package api -generate types,chi-server -o server.gen.go openapi.yaml`
- `oapi-codegen -config oapi-codegen.yaml openapi.yaml`
- `go build ./...`

**Examples:**
- -generate types,client emits a typed Go client
- -generate chi-server emits a server stub
- -config uses a YAML config file

### go-testing
Test the generated Go client

**Commands:**
- `go test ./...`
- `go vet ./...`
- `go mod tidy`
- `go test -race ./...`

**Examples:**
- -cli --help
- -api --help

## References
- [oapi-codegen](https://github.com/oapi-codegen/oapi-codegen)
- [Go Tooling](https://go.dev/doc/modules/)
