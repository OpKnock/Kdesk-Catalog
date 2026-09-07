---
name: "autocannon"
description: "Load-tests HTTP servers with autocannon: concurrent connections, custom methods/bodies, latency reports, and JSON output. Use when working with basic load, custom requests, reporting, api or when the user mentions basic load, custom requests, reporting, api."
license: "MIT"
compatibility: "Requires npx."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

Load-tests HTTP servers with autocannon: concurrent connections, custom methods/bodies, latency reports, and JSON output.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx autocannon -c 100 -d 30 http://localhost:3000`, `npx autocannon -c 50 -d 20 -m POST -b '{"name":"test"}' -H "`
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

# Autocannon

## What this skill does

Load-tests HTTP servers with autocannon: concurrent connections, custom methods/bodies/headers, latency percentiles, status-code breakdowns, and JSON results for CI.

## When to use

- Quick capacity check of an endpoint
- Comparing latency before/after an optimization
- Verifying a server survives burst connections

## Real commands

```bash
# Basic: 100 connections for 30s
npx autocannon -c 100 -d 30 http://localhost:3000

# With latency breakdown
npx autocannon -c 50 -d 60 --latency http://localhost:3000

# POST with JSON body
npx autocannon -c 50 -d 20 -m POST -b '{"name":"test"}' -H "Content-Type: application/json" http://localhost:3000/api/users

# JSON output for CI
npx autocannon --json -c 100 -d 20 http://localhost:3000 > results.json

# Extract p99
npx autocannon --json http://localhost:3000 | jq '.latency.p99'
```

## Testing

- Run once to warm up, then record the second run
- Compare results across commits; guard on p99 regressions

## Best practices

- Fix the target rate (-R) or connections (-c) for comparability
- Test with real payloads, not empty GETs
- Watch for socket errors and timeouts, not just throughput

## Capabilities

### basic-load
Run basic load tests with configurable concurrency and duration.

**Parameters:**
- `connections` (number): Concurrent connections (-c)
- `duration` (number): Test duration in seconds (-d)
- `rate` (number): Fixed requests per second (-R)

**Commands:**
- `npx autocannon -c 100 -d 30 http://localhost:3000`
- `npx autocannon -c 50 -d 60 --latency http://localhost:3000`
- `npx autocannon -R 1000 http://localhost:3000`
- `npx autocannon --workers 4 -c 100 -d 30 http://localhost:3000`

**Examples:**
- npx autocannon -c 100 -d 30 http://localhost:3000
- npx autocannon --latency -c 20 -d 120 http://localhost:3000/api/users
- npx autocannon -c 1000 --duration 10 http://localhost:3000/health

### custom-requests
Load-test with custom methods, bodies, headers, and paths.

**Parameters:**
- `method` (string): HTTP method (-m)
- `body` (string): Request body (-b)
- `headers` (string): Headers as -H key:value

**Commands:**
- `npx autocannon -c 50 -d 20 -m POST -b '{"name":"test"}' -H "Content-Type: application/json" http://localhost:3000/api/users`
- `npx autocannon -c 50 -d 20 -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/me`
- `npx autocannon -c 10 -d 30 --body '{"q":"search"}' -m POST -H "Content-Type: application/json" http://localhost:3000/api/search`
- `npx autocannon -c 20 -d 30 -m PUT -b '{"status":"ok"}' -H "Content-Type: application/json" http://localhost:3000/api/orders/42`

**Examples:**
- npx autocannon -c 50 -d 20 -m POST -b '{"name":"test"}' -H "Content-Type: application/json" http://localhost:3000/api/users
- npx autocannon --connections 100 -m PATCH -b '{"seen":true}' -H "Content-Type: application/json" http://localhost:3000/api/notifications/1
- npx autocannon -c 10 -d 60 -H "Accept: application/json" http://localhost:3000/api/feed

### reporting
Capture JSON results and render reports.

**Parameters:**
- `json` (boolean): Emit JSON output
- `output` (string): Write results to a file

**Commands:**
- `npx autocannon --json -c 100 -d 20 http://localhost:3000 > results.json`
- `npx autocannon --output results.json -c 100 -d 20 http://localhost:3000`
- `npx autocannon -c 100 -d 20 http://localhost:3000 | jq '.latency'`
- `npx autocannon -c 100 -d 20 --renderStatusCodes http://localhost:3000`

**Examples:**
- npx autocannon --json http://localhost:3000 | jq '{requests, latency: .latency.p99}'

- npx autocannon --output results.json -d 30 -c 100 http://localhost:3000 && cat results.json | jq .requests
- npx autocannon --renderStatusCodes -c 50 -d 10 http://localhost:3000

## References
- [autocannon GitHub](https://github.com/mcollina/autocannon)
- [Node.js Benchmarking Guide](https://nodejs.org/en/learn/diagnostics/simple-profiling)
