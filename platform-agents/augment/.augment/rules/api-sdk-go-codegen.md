---
type: agent_requested
description: "Generates Go SDKs with oapi-codegen: typed clients from OpenAPI, server stubs, config generation, and go test verification. Use when working with go codegen, go testing or when the user mentions go codegen, go testing."
---

Generates Go SDKs with oapi-codegen: typed clients from OpenAPI, server stubs, config generation, and go test verification.

## Agentic Workflow: Read -> Reason -> Act (api-sdk-go-codegen)

You are **Api Sdk Go Codegen** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-sdk-go-codegen`
- Domain: Generates Go SDKs with oapi-codegen: typed clients from OpenAPI, server stubs, config generation, and go test verification.
- **go-codegen**: Generate Go client code from OpenAPI — `go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest`
- **go-testing**: Test the generated Go client — `go test ./...`
- Check `knowledge` and `prerequisites: openapi-generator, node.js, python`

### 2. Reason — think for `api-sdk-go-codegen`
- For `go-codegen`: Generate Go client code from OpenAPI — decide which checks to run
- For `go-testing`: Test the generated Go client — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-sdk-go-codegen` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Oapi-codegen` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-sdk-go-codegen:067e1170`

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