---
applyTo: "**/*.json **/*.r **/*.sh"
---

# load-testing-engineer

Designs and executes load tests with k6, Vegeta, and wrk: scenarios, thresholds, and CI-integrated performance gates.

## Instructions

# Load Testing

Prove capacity before customers do.

## When to Use

- Launch and marketing-event capacity planning
- Verifying perf fixes and regressions
- Establishing baseline per release

## k6 scenarios

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01']
  }
};

export default function () {
  const res = http.get('http://localhost:8080/api');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

```bash
k6 run --vus 50 --duration 1m load-test.js
```

Thresholds make tests fail automatically - use them in CI.

## Test types

- Smoke: 1-5 VUs, validate plumbing.
- Load: 50-200 VUs, expected peak.
- Stress: ramp until failure; find the ceiling.
- Soak: 1h+, catch leaks.

## Vegeta quick report

```bash
echo 'GET http://localhost:8080/' | vegeta attack -rate=200 -duration=30s | vegeta report
```

## Reading results

- Latency: watch p95/p99, not mean.
- Errors: check rate threshold, not absolute count.
- Compare against the recorded baseline per release.

## Best practices

- Never load test production without approval; use staging.
- Correlate with server metrics (CPU, pool depth, DB).
- Freeze code and config during the run.
- Store results with the release tag for regression diffing.

## Testing

```bash
k6 run --vus 20 --duration 30s --summary-trend-stats='avg,p(95),p(99)' smoke.js
```

Gate the pipeline on thresholds.

## Capabilities

### k6
Write and run scripted load tests with k6.

**Commands:**
- `k6 run --vus 50 --duration 1m load-test.js`
- `k6 inspect load-test.js`
- `k6 run --vus 20 --duration 30s --summary-trend-stats='avg,p(95),p(99)' load-test.js`
- `k6 run --out json=results.json load-test.js`
- `k6 run --vus 100 --duration 2m --execution-segment=1/3:2/3 load-test.js`

**Examples:**
- k6 run --vus 50 --duration 1m --out influxdb=http://localhost:8086/k6 smoke.js
- k6 run --summary-trend-stats='p(99)' soak.js
- k6 inspect smoke.js | jq '.config.options.vus'

### vegeta
Attack endpoints with Vegeta and generate reports.

**Commands:**
- `echo 'GET http://localhost:8080/' | vegeta attack -rate=200 -duration=30s | vegeta report`
- `echo 'POST http://localhost:8080/api' | vegeta attack -header 'Content-Type: application/json' -body payload.json -rate=100 -duration=60s | vegeta report -type=json > report.json`
- `vegeta attack -targets=targets.txt -rate=500 -duration=30s | vegeta report -type=hist[0,100ms,200ms,500ms]`
- `vegeta attack -rate=50 -duration=1m | vegeta report -type=text`
- `vegeta attack -targets=targets.txt -rate=100 -duration=30s -timeout=10s | vegeta report`

**Examples:**
- echo 'GET http://localhost:8080/healthz' | vegeta attack -rate=1000 -duration=10s | vegeta report
- vegeta attack -targets=targets.txt -rate=300 -duration=1m | vegeta report -type=json | jq '.latencies'
- echo 'GET http://localhost:8080/' | vegeta attack -rate=100 -duration=30s | vegeta plot > plot.html
