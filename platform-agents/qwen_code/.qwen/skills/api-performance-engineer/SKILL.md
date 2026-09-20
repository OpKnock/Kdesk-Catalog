---
name: "api-performance-engineer"
description: "Engineers API performance end-to-end with vegeta: attack targets files, rate/duration attacks, histogram reports, and binary result encoding for charting."
---

# api-performance-engineer

Engineers API performance end-to-end with vegeta: attack targets files, rate/duration attacks, histogram reports, and binary result encoding for charting.

## Instructions

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
