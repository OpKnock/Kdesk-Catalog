---
type: agent_requested
description: "Builds backend services in Go: module management, testing, benchmarking, profiling, and race detection."
---

# go

Builds backend services in Go: module management, testing, benchmarking, profiling, and race detection.

## Instructions

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