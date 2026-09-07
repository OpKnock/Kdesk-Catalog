---
name: "profiling"
description: "CPU and memory profiling: perf record/report, Go pprof, and flamegraph generation. Use when working with profiling analysis, api or when the user mentions profiling analysis, api."
license: "MIT"
compatibility: "Requires perf."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(go:*) Bash(perf:*)"
---

CPU and memory profiling: perf record/report, Go pprof, and flamegraph generation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `perf record -g ./myapp`
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

# Profiling

Find where CPU time and memory actually go with sampling profilers.

## What this skill does

- Records CPU profiles with perf
- Reads Go pprof endpoints
- Visualizes results

## When to use

- High CPU usage or latency mysteries
- Memory growth investigations

## Real commands

```bash
# perf
perf record -g ./myapp
perf record -g -p 1234 -- sleep 60
perf report --stdio
perf top

# Go pprof (app must import net/http/pprof)
go tool pprof -top http://localhost:6060/debug/pprof/heap
go tool pprof -top http://localhost:6060/debug/pprof/cpu
go tool pprof -http=:8081 http://localhost:6060/debug/pprof/profile
go tool pprof -http=:8081 http://localhost:6060/debug/pprof/goroutine
```

## Reading results

- Flat: time in this function; Cum: including callees
- Look for hot call chains, not just hot functions

## Best practices

- Profile under production-like load
- Capture 30-60s windows
- Compare profiles before/after optimizations

## Capabilities

### profiling-analysis
Capture CPU profiles with perf, analyze Go profiles with pprof, and visualize as flamegraphs.

**Parameters:**
- `pid` (integer): Process ID to profile
- `profile_source` (string): pprof URL or profile file
- `duration` (string): Capture duration

**Commands:**
- `perf record -g ./myapp`
- `perf report --stdio`
- `perf top`
- `go tool pprof -top http://localhost:6060/debug/pprof/heap`
- `go tool pprof -http=:8081 http://localhost:6060/debug/pprof/profile`

**Examples:**
- perf record -g -p 1234 -- sleep 60
- go tool pprof -top http://localhost:6060/debug/pprof/cpu
- go tool pprof -http=:8081 http://localhost:6060/debug/pprof/goroutine

## References
- [perf wiki](https://perf.wiki.kernel.org/index.php/Main_Page)
- [pprof docs](https://pkg.go.dev/net/http/pprof)
