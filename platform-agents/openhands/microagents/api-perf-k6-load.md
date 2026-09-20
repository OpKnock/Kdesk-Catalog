---
name: "api-perf-k6-load"
description: "Runs k6 load tests against APIs: virtual users, stages, thresholds, checks, and CI-friendly summary exports for throughput and latency assertions."
type: knowledge
triggers: ["api-perf-k6-load", "k6-load-testing", "thresholds-checks"]
---

# Api Perf K6 Load

Runs k6 load tests against APIs: virtual users, stages, thresholds, checks, and CI-friendly summary exports for throughput and latency assertions.

## Instructions

# API Perf v2 - k6 Load Testing

Load testing with k6.

## What This Skill Does
- Simulates realistic user load with virtual users
- Ramps traffic in stages to find saturation
- Fails CI when thresholds are breached

## When to Use
- Before releases to catch regressions
- Capacity planning for expected traffic
- Comparing architecture options (caching, scaling)

## Real Commands

```bash
k6 run --vus 50 --duration 60s script.js
k6 run --stage '2s:10,30s:100,10s:0' ramping.js
k6 run --summary-export=summary.json script.js
```

## Script Example

```js
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<300'] }
};
export default function () {
  const res = http.get('https://api.example.com/v1/items');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Testing
- Run a soak variant (30m at moderate load) for leaks
- Add scenarios to mix read and write traffic
- Use k6 inspect to validate options before full runs

## Best Practices
- Randomize test data to avoid cache skewing results
- Set thresholds on percentiles, not averages
- Store summary.json outputs for regression charts

## Capabilities

### k6-load-testing
Execute scripted load tests with thresholds

**Commands:**
- `k6 run script.js`
- `k6 run --vus 50 --duration 60s script.js`
- `k6 run --stage '2s:10,30s:100,10s:0' ramping.js`
- `k6 run --summary-export=summary.json script.js`
- `k6 inspect script.js`

**Examples:**
- k6 run --vus 50 --duration 60s runs a steady 50-user load
- --stage ramps users up and down over time
- --summary-export writes JSON for CI comparison

### thresholds-checks
Define pass/fail gates on latency and error rate

**Commands:**
- `k6 run --threshold 'http_req_duration:p(95)<300' script.js`
- `k6 run --threshold 'http_req_failed:rate<0.01' script.js`
- `k6 run --quiet script.js`

**Examples:**
- -cli --help
- -api --help
