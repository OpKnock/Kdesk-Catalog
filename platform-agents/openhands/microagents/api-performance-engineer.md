---
name: "api-performance-engineer"
description: "Engineers API performance end-to-end with vegeta: attack targets files, rate/duration attacks, histogram reports, and binary result encoding for charting. Use when working with vegeta attacks, distributed attacks or when the user mentions vegeta attacks, distributed attacks."
type: knowledge
triggers: ["api-performance-engineer", "vegeta-attacks", "distributed-attacks"]
---

Engineers API performance end-to-end with vegeta: attack targets files, rate/duration attacks, histogram reports, and binary result encoding for charting.

## Agentic Workflow: Read -> Reason -> Act (api-performance-engineer)

You are **api-performance-engineer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-performance-engineer`
- Domain: Engineers API performance end-to-end with vegeta: attack targets files, rate/duration attacks, histogram reports, and binary result encoding for charting.
- **vegeta-attacks**: Run vegeta load attacks from targets files — `echo "GET http://localhost:3000/api" | vegeta attack -duration=30s -rate=100 | v`
- **distributed-attacks**: Scale attacks across machines with vegeta — `vegeta attack -rate=0 -max-workers=10 -duration=60s -targets=targets.txt > resul`
- Check `knowledge` and `prerequisites: node.js, python, redis, new-relic`

### 2. Reason — think for `api-performance-engineer`
- For `vegeta-attacks`: Run vegeta load attacks from targets files — decide which checks to run
- For `distributed-attacks`: Scale attacks across machines with vegeta — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-performance-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Echo`, `Vegeta` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-performance-engineer:334ac477`

# API Performance Engineer

Load engineering with vegeta.

## What This Skill Does
- Runs fixed-rate attacks with exact QPS control
- Reports histograms, percentiles, and status code distributions
- Produces artifacts for dashboards and reports

## When to Use
- Precise rate-based capacity tests
- Comparing versions with identical attack profiles
- Generating shareable performance reports

## Real Commands

```bash
echo "GET http://localhost:3000/api" | vegeta attack -duration=30s -rate=100 | vegeta report
vegeta attack -targets=targets.txt -rate=50 -duration=60s | tee results.bin | \
  vegeta report -type=hist[0,10ms,50ms,200ms,1s]
vegeta encode -to json < results.bin | jq '.[0].latencies'
```

## Targets File

```
GET http://localhost:3000/api/items
POST http://localhost:3000/api/items
Content-Type: application/json
@/tmp/body.json
```

## Testing
- Verify attack rate matches configured QPS
- Correlate latency percentiles with resource utilization
- Keep result binaries for reproducible audits

## Best Practices
- Use -max-workers to control concurrency beyond rate
- Name attacks to identify test scenarios
- Store report.json in CI artifacts per release

## Capabilities

### vegeta-attacks
Run vegeta load attacks from targets files

**Parameters:**
- `rate` (integer): Requests per second
- `duration` (string): Attack duration like 30s
- `targets-file` (string): File with method/url/header lines

**Commands:**
- `echo "GET http://localhost:3000/api" | vegeta attack -duration=30s -rate=100 | vegeta report`
- `vegeta attack -targets=targets.txt -rate=50 -duration=60s -name=apiv1 | tee results.bin | vegeta report -type=hist[0,10ms,50ms,200ms,1s]`
- `vegeta encode -to json < results.bin | jq '.[0].latencies'`
- `vegeta report -type=json results.bin > report.json`
- `vegeta plot results.bin > plot.html`

**Examples:**
- vegeta attack pipes directly into vegeta report
- hist[0,10ms,...] groups latency into buckets
- vegeta plot generates an interactive HTML chart

### distributed-attacks
Scale attacks across machines with vegeta

**Commands:**
- `vegeta attack -rate=0 -max-workers=10 -duration=60s -targets=targets.txt > results.bin`
- `vegeta report -every=5s results.bin`
- `vegeta dump results.bin | head -5`

**Examples:**
- -cli --help
- -api --help

## References
- [vegeta GitHub](https://github.com/tsenart/vegeta)
- [vegeta Target Format](https://github.com/tsenart/vegeta/blob/master/README.md#target-format)
