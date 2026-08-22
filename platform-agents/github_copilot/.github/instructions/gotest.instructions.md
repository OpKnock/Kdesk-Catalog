---
applyTo: "**/*.go **/*.html **/*.r **/*.sh"
---

# gotest

Runs Go tests with go test, covering race detection, coverage profiles, benchmarks, and focused runs.

## Instructions

# go test

Testing Go code with the standard toolchain.

## What This Skill Does

- Runs unit and integration tests with filters
- Detects data races with -race
- Produces and visualizes coverage profiles
- Runs benchmarks with memory stats

## When to Use

- Pre-merge test verification
- Race condition debugging
- Performance regression checks

## Real Commands

```bash
# Basics
 go test ./...
go test -v ./internal/...
go test -run TestOrderService ./...
go test -count=1 ./...

# Race detection
go test -race ./...

# Coverage
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
go tool cover -html=coverage.out

# Benchmarks
go test -bench=. -benchmem ./...
go test -bench=BenchmarkParse -benchtime=5s

# Lint
go vet ./...
```

## Sample Test

```go
func TestParse(t *testing.T) {
	got, err := Parse("42")
	if err != nil {
		t.Fatal(err)
	}
	if got != 42 {
		t.Errorf("Parse() = %d, want 42", got)
	}
}
```

## Best Practices

- Use table-driven tests with t.Run subtests
- Run -race in CI; races are bugs
- Set coverage gates via go tool cover -func
- Use -count=1 to avoid cached results during debugging
- Benchmark against a fixed revision for comparisons

## Capabilities

### go-testing
Run Go tests with filters and verbosity.

**Commands:**
- `go test ./...`
- `go test -v ./internal/...`
- `go test -run TestOrderService ./...`
- `go test -count=1 ./...`
- `go test -short ./...`

**Examples:**
- go test ./...
- go test -run TestOrderService -v ./internal/orders
- go test -count=1 ./...

### race-and-coverage
Race detection and coverage profiles.

**Commands:**
- `go test -race ./...`
- `go test -coverprofile=coverage.out ./...`
- `go tool cover -func=coverage.out`
- `go tool cover -html=coverage.out`
- `go test -covermode=atomic ./...`

**Examples:**
- go test -race ./...
- go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out
- go tool cover -html=coverage.out

### benchmarks-and-vet
Benchmarks, profiling, and vet checks.

**Commands:**
- `go test -bench=. -benchmem ./...`
- `go test -bench=BenchmarkParse -benchtime=5s ./...`
- `go vet ./...`
- `go test -run=NONE -bench=. ./...`
- `go test -cpuprofile=cpu.out -bench=. ./...`

**Examples:**
- go test -bench=. -benchmem ./...
- go vet ./...
- go test -bench=BenchmarkParse -benchtime=5s
