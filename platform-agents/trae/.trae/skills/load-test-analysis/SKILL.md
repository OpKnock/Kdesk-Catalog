---
name: "load-test-analysis"
description: "Analyze load test results: extract percentiles from k6/hey/ab outputs, compute error rates, and summarize performance regressions."
---

# Load Test Analysis

Analyze load test results: extract percentiles from k6/hey/ab outputs, compute error rates, and summarize performance regressions.

## Instructions

# Load Test Analysis

Turn load test output into actionable performance signals.

## What this skill does

- Extracts p(95)/p(99) latency and error rates from results.
- Compares baseline vs. regression runs.
- Computes throughput from raw counters.

## When to use

- Post-load-test triage: did this release regress?
- Building perf dashboards from k6/ab/hey outputs.
- Writing CI gates on percentile thresholds.

## Real commands

```bash
# k6 run with export
k6 run --summary-export=summary.json load.js

# p(95) latency
jq '.metrics.http_req_duration.values["p(95)"]' summary.json

# Error rate
jq '.metrics.http_req_failed.values.rate' summary.json

# Throughput (req/s)
jq '.metrics.http_reqs.values.count / .metrics.http_req_duration.values.avg' summary.json

# hey percentile
hey -n 5000 -c 100 http://localhost:8080/ | grep '95% in'

# ab summary
ab -n 10000 -c 200 -k http://localhost:8080/ | grep -E 'Requests per second|Failed requests'

# Compare two ab runs
awk '/^Requests per second/{print $4}' ab-before.txt ab-after.txt

# Tight stats for CI gates
k6 run --summary-trend-stats='avg,p(99.9)' load.js
```

## Example analysis workflow

```bash
k6 run --summary-export=before.json load.js
# ... deploy change ...
k6 run --summary-export=after.json load.js
jq -n --argjson b "$(cat before.json)" --argjson a "$(cat after.json)"   '{p95_delta: ($a.metrics.http_req_duration.values["p(95)"] - $b.metrics.http_req_duration.values["p(95)"]),
    err_delta: ($a.metrics.http_req_failed.values.rate - $b.metrics.http_req_failed.values.rate)}'
```

## Testing

```bash
jq -e '.metrics.http_req_duration.values["p(95)"] < 300' summary.json && echo PASS
```

## Best practices

- Always capture a baseline under identical load profiles.
- Report p(95)/p(99) plus error rate; averages hide tail pain.
- Store summaries with run metadata (commit, env) for trend analysis.

## Capabilities

### percentile-analysis
Extract latency percentiles from k6 JSON exports and CLI summaries.

**Commands:**
- `k6 run --summary-export=summary.json load.js`
- `jq '.metrics.http_req_duration.values["p(95)"]' summary.json`
- `jq '.metrics.http_req_failed.values.rate' summary.json`
- `hey -n 5000 -c 100 http://localhost:8080/ | grep '95% in'`

**Examples:**
- k6 run --summary-export=summary.json load.js
- jq '.metrics.http_req_duration.values["p(95)"]' summary.json
- hey -n 5000 -c 100 http://localhost:8080/ | grep '95% in'

### compare-runs
Compare baseline vs. after runs and summarize throughput/errors.

**Commands:**
- `ab -n 10000 -c 200 -k http://localhost:8080/ | grep -E 'Requests per second|Failed requests'`
- `jq '.metrics.http_reqs.values.count / .metrics.http_req_duration.values.avg' summary.json`
- `awk '/^Requests per second/{print $4}' ab-before.txt ab-after.txt`
- `k6 run --summary-trend-stats='avg,p(99.9)' load.js`

**Examples:**
- ab -n 10000 -c 200 -k http://localhost:8080/ | grep -E 'Requests per second|Failed requests'
- awk '/^Requests per second/{print $4}' ab-before.txt ab-after.txt
- jq '.metrics.http_reqs.values.count / .metrics.http_req_duration.values.avg' summary.json
