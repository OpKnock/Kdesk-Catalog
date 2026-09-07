---
trigger: glob
description: "Builds backend services in Go: module management, testing, benchmarking, profiling, and race detection. Use when working with go build, go testing, backend or when the user mentions go build, go testing, backend."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

Builds backend services in Go: module management, testing, benchmarking, profiling, and race detection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go mod init localhost/myapp`, `go test ./...`
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

# Go

Backend development with the Go toolchain.

## When to Use

- High-concurrency services (HTTP, gRPC, workers)
- CLIs and infrastructure tooling
- Systems where memory and startup matter
- Services that benefit from static binaries

## Commands

```bash
# Module init
go mod init example.com/myapp

# Build and vet
go build ./...
go vet ./...

# Tests
go test ./...
go test -race ./...
go test -cover ./...

# Benchmarks
go test -bench=. -benchmem ./internal/parse

# Run and install
go run ./cmd/app
go install ./cmd/app
```

## HTTP Server

```go
package main

import (
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok"))
	})
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## Best Practices

- Always run go test -race in CI to catch data races
- Keep the public API of packages small; export only what is needed
- Use context for cancellation and timeouts in handlers and clients
- Run gofmt/go vet before every commit
- Prefer errgroup for running independent goroutines with error propagation
- Pin dependencies in go.mod and update with go get -u then go mod tidy

## Capabilities

### go-build
Create modules, build, vet, and install Go programs.

**Parameters:**
- `package` (string): Package pattern to build
- `output` (string): Binary output path

**Commands:**
- `go mod init localhost/myapp`
- `go build ./...`
- `go vet ./...`
- `go install ./cmd/app`
- `go run ./cmd/app`

**Examples:**
- go build -o bin/app ./cmd/app
- go mod tidy
- go vet -v ./...

### go-testing
Run tests, benchmarks, and race detection.

**Parameters:**
- `run` (string): Regex matching test names
- `bench` (string): Regex matching benchmarks
- `cover` (boolean): Collect coverage

**Commands:**
- `go test ./...`
- `go test -race ./...`
- `go test -cover ./...`
- `go test -bench=. -benchmem ./internal/parse`
- `go test -run TestParse -v`

**Examples:**
- go test -race -count=1 ./...
- go test -bench=BenchmarkParse -benchmem -run ^$ ./...
- go test -coverprofile=coverage.out ./...

## References
- [Go Docs](https://go.dev/doc/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Testing Package](https://pkg.go.dev/testing)
