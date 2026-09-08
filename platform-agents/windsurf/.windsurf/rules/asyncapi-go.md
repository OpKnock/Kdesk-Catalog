---
trigger: glob
description: "Generates Go models and typed publisher/subscriber code from AsyncAPI documents using Modelina and asyncapi-go. Use when working with go generation, asyncapi go codegen or when the user mentions go generation, asyncapi go codegen."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Generates Go models and typed publisher/subscriber code from AsyncAPI documents using Modelina and asyncapi-go.

## Agentic Workflow: Read -> Reason -> Act (asyncapi-go)

You are **Asyncapi Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `asyncapi-go`
- Domain: Generates Go models and typed publisher/subscriber code from AsyncAPI documents using Modelina and asyncapi-go.
- **go-generation**: Generate Go types from an AsyncAPI spec with Modelina. — `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./internal/models`
- **asyncapi-go-codegen**: Produce typed publisher/subscriber interfaces with asyncapi-go. — `go install github.com/lerayjin/asyncapi-go@latest`
- Check `knowledge` and `prerequisites: asyncapi-go, gofmt, npx`

### 2. Reason — think for `asyncapi-go`
- For `go-generation`: Generate Go types from an AsyncAPI spec with Modelina. — decide which checks to run
- For `asyncapi-go-codegen`: Produce typed publisher/subscriber interfaces with asyncapi-go. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `asyncapi-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `asyncapi-go:f1dac5c4`

# AsyncAPI Go

## What this skill does

Generates Go code from AsyncAPI documents: typed models via Modelina and publisher/subscriber interfaces via asyncapi-go, wired into a working Go service.

## When to use

- A Go microservice must publish/consume events from a spec
- Bootstrapping typed message handling without hand-writing structs
- Keeping Go payloads in sync with an evolving spec

## Real commands

```bash
# Generate Go models
npx @asyncapi/modelina generate --input asyncapi.yaml --output ./internal/models --language Go --packageName orderapi

# Init module and build
go mod init github.com/example/order-service
go build ./...
go vet ./...

# Generate typed channels
asyncapi-go generate --input asyncapi.yaml --output ./gen

# Run a subscriber
go run ./cmd/subscriber --broker kafka://localhost:9092
```

## Generated struct

```go
package orderapi

type OrderCreated struct {
	ID     string  `json:"id"`
	Amount float64 `json:"amount"`
}
```

## Testing

- go test ./... -race for handler concurrency
- Publish with a producer, assert the subscriber receives the same JSON

## Best practices

- Regenerate in CI and fail on drift with git diff --exit-code
- Keep packageName consistent with module layout
- Never edit generated files; extend via composition

## Capabilities

### go-generation
Generate Go types from an AsyncAPI spec with Modelina.

**Parameters:**
- `package_name` (string): Go package name for generated models
- `module` (string): Go module path for go mod init

**Commands:**
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./internal/models --language Go`
- `go mod init github.com/example/order-service`
- `go build ./...`
- `go vet ./...`
- `go test ./...`

**Examples:**
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./internal/models --language Go --packageName orderapi
- go mod init github.com/example/order-service && go build ./...
- go test ./internal/... -race

### asyncapi-go-codegen
Produce typed publisher/subscriber interfaces with asyncapi-go.

**Parameters:**
- `input` (string): AsyncAPI document path
- `output` (string): Output directory
- `broker` (string): Broker URL, e.g. kafka://localhost:9092

**Commands:**
- `go install github.com/lerayjin/asyncapi-go@latest`
- `asyncapi-go generate --input asyncapi.yaml --output ./gen`
- `gofmt -l ./gen`
- `go run ./cmd/subscriber --broker kafka://localhost:9092`
- `curl -s http://localhost:8080/metrics`

**Examples:**
- asyncapi-go generate --input asyncapi.yaml --output ./gen --package gen
- gofmt -w ./gen && go vet ./gen/...
- go run ./cmd/subscriber --broker kafka://localhost:9092

## References
- [Modelina Go](https://www.asyncapi.com/docs/tools/modelina/languages/Go)
- [asyncapi-go](https://github.com/lerayjin/asyncapi-go)
- [AsyncAPI for Go](https://www.asyncapi.com/docs/tutorials/getting-started/go)
