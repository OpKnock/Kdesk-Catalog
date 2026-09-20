Runs Go tests with go test, covering race detection, coverage profiles, benchmarks, and focused runs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go test ./...`, `go test -race ./...`
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