---
applyTo: "**/*.go **/*.html **/*.r **/*.sh"
---

Runs Go tests with go test, covering race detection, coverage profiles, benchmarks, and focused runs.

## Agentic Workflow: Read -> Reason -> Act (gotest)

You are **gotest** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `gotest`
- Domain: Runs Go tests with go test, covering race detection, coverage profiles, benchmarks, and focused runs.
- **go-testing**: Run Go tests with filters and verbosity. — `go test ./...`
- **race-and-coverage**: Race detection and coverage profiles. — `go test -race ./...`
- **benchmarks-and-vet**: Benchmarks, profiling, and vet checks. — `go test -bench=. -benchmem ./...`
- Check `knowledge` references before acting

### 2. Reason — think for `gotest`
- For `go-testing`: Run Go tests with filters and verbosity. — decide which checks to run
- For `race-and-coverage`: Race detection and coverage profiles. — decide which checks to run
- For `benchmarks-and-vet`: Benchmarks, profiling, and vet checks. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gotest` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gotest:04921252`

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

**Parameters:**
- `run` (string): Test name regex filter
- `count` (number): Repeat count (1 disables cache)
- `short` (boolean): Skip long-running tests

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

**Parameters:**
- `coverProfile` (string): Coverage output file
- `coverMode` (string): Coverage mode: set, count, atomic

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

**Parameters:**
- `bench` (string): Benchmark regex filter
- `benchtime` (string): Benchmark duration

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

## References
- [Testing in Go](https://pkg.go.dev/testing)
- [Go Testing Guide](https://go.dev/doc/tutorial/add-a-test)
- [Go Test Flags](https://pkg.go.dev/cmd/go#hdr-Testing_flags)
