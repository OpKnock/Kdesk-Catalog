---
name: "asyncapi-go"
description: "Generates Go models and typed publisher/subscriber code from AsyncAPI documents using Modelina and asyncapi-go. Use when working with go generation, asyncapi go codegen or when the user mentions go generation, asyncapi go codegen."
license: "MIT"
compatibility: "Requires asyncapi-go, gofmt, npx. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(asyncapi-go:*) Bash(curl:*) Bash(go:*) Bash(gofmt:*) Bash(npx:*)"
---

Generates Go models and typed publisher/subscriber code from AsyncAPI documents using Modelina and asyncapi-go.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @asyncapi/modelina generate --input asyncapi.yaml --outp`, `go install github.com/lerayjin/asyncapi-go@latest`
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
