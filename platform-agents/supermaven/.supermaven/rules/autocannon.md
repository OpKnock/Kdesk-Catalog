Load-tests HTTP servers with autocannon: concurrent connections, custom methods/bodies, latency reports, and JSON output.

## Agentic Workflow: Read -> Reason -> Act (autocannon)

You are **Autocannon** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `autocannon`
- Domain: Load-tests HTTP servers with autocannon: concurrent connections, custom methods/bodies, latency reports, and JSON output.
- **basic-load**: Run basic load tests with configurable concurrency and duration. — `npx autocannon -c 100 -d 30 http://localhost:3000`
- **custom-requests**: Load-test with custom methods, bodies, headers, and paths. — `npx autocannon -c 50 -d 20 -m POST -b '{"name":"test"}' -H "Content-Type: applic`
- **reporting**: Capture JSON results and render reports. — `npx autocannon --json -c 100 -d 20 http://localhost:3000 > results.json`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `autocannon`
- For `basic-load`: Run basic load tests with configurable concurrency and duration. — decide which checks to run
- For `custom-requests`: Load-test with custom methods, bodies, headers, and paths. — decide which checks to run
- For `reporting`: Capture JSON results and render reports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `autocannon` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `autocannon:e44450c6`

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