---
trigger: glob
description: "Analyzes API latency distribution and connection behavior with autocannon, artillery quick mode, and request-level timing to separate network from application cost."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Api Perf Autocannon

Analyzes API latency distribution and connection behavior with autocannon, artillery quick mode, and request-level timing to separate network from application cost.

## Instructions

# API Perf v4 - Latency Analysis

Latency distribution analysis with autocannon.

## What This Skill Does
- Measures latency percentiles with pipelining control
- Produces JSON artifacts for trend tracking
- Drives ad-hoc loads with artillery quick

## When to Use
- Verifying latency improvements after a fix
- Comparing request sizes and connection reuse
- Ad-hoc load checks without writing scripts

## Real Commands

```bash
npx autocannon -c 20 -d 30 -p 1 http://localhost:3000/
npx autocannon --json http://localhost:3000/ > results.json
npx artillery quick -d 30 -r 20 http://localhost:3000/api
```

## Interpreting Output
- avg/max: central and worst-case latency
- p1-p99: full distribution shape
- errors: connection and timeout failures
- requests/sec: achieved throughput

## Testing
- Repeat runs 3x and compare medians
- Vary payload size to expose serialization cost
- Test HTTP/1.1 vs HTTP/2 if both available

## Best Practices
- Keep -p 1 for mobile-like latency measurements
- Persist JSON outputs per build for regression charts
- Correlate latency shifts with deploy timestamps

## Capabilities

### autocannon
Run pipelined HTTP benchmarks with full statistics

**Commands:**
- `npx autocannon -c 20 -d 30 -p 1 http://localhost:3000/`
- `npx autocannon -c 10 -d 20 -m POST -b '{"a":1}' -H 'Content-Type=application/json' http://localhost:3000/api`
- `npx autocannon -c 20 -d 30 --json http://localhost:3000/ > results.json`
- `npx autocannon --renderStatusCodes -c 20 -d 10 http://localhost:3000/`

**Examples:**
- autocannon -p 1 disables pipelining for realistic latency
- --json emits machine-readable results for charts
- --renderStatusCodes shows the status code mix

### artillery-quick
Use artillery quick for ad-hoc load scenarios

**Commands:**
- `npx artillery quick -d 30 -r 20 http://localhost:3000/api`
- `npx artillery quick --count 50 --num 20 http://localhost:8080/users`
- `npx artillery quick -d 60 -r 50 -o report.json http://localhost:3000/`

**Examples:**
- -cli --help
- -api --help
