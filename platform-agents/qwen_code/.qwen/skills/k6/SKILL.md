---
name: "k6"
description: "Load-tests APIs with k6 scripts, scenarios, thresholds, and Grafana Cloud reporting."
---

# k6

Load-tests APIs with k6 scripts, scenarios, thresholds, and Grafana Cloud reporting.

## Instructions

# k6

Load testing with developer-friendly JavaScript scripts.

## What This Skill Does

- Runs scenarios with virtual users, iterations, and ramps
- Asserts SLOs with thresholds
- Exports JSON/cloud results
- Archives tests for reproducibility

## When to Use

- Capacity planning and soak tests
- SLO validation under load
- API regression performance checks

## Real Commands

```bash
# Run
k6 run script.js
k6 run -u 100 -d 30s script.js
k6 run --iterations 1000 script.js
k6 run --env BASE_URL=https://staging.example.com script.js

# Outputs
k6 run --summary-trend-stats="avg,p(95),p(99)" script.js
k6 run --out json=results.json script.js

# Cloud
k6 login cloud
k6 cloud run script.js
```

## Sample Script

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    load: { executor: 'ramping-vus', stages: [
      { duration: '1m', target: 50 },
      { duration: '5m', target: 200 },
      { duration: '1m', target: 0 }
    ]}
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500']
  }
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/v1/products`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Best Practices

- Ramp VUs gradually; test both steady state and spikes
- Set thresholds that mirror SLOs
- Check p(95)/p(99), not just averages
- Use __ENV for environment-specific URLs
- Archive scripts for reproducible runs

## Capabilities

### k6-runs
Run k6 test scripts with virtual users and durations.

**Commands:**
- `k6 run script.js`
- `k6 run -u 100 -d 30s script.js`
- `k6 run --vus 50 --duration 2m script.js`
- `k6 run --iterations 1000 script.js`
- `k6 run --env BASE_URL=http://localhost:8080 script.js`

**Examples:**
- k6 run -u 100 -d 30s script.js
- k6 run --iterations 1000 script.js
- k6 run --env BASE_URL=http://localhost:8080 script.js

### thresholds-and-reports
Assert performance and export results.

**Commands:**
- `k6 run --summary-trend-stats="avg,p(95),p(99)" script.js`
- `k6 run --out json=results.json script.js`
- `k6 run --out web-dashboard script.js`
- `k6 run --tag env=staging script.js`
- `k6 login cloud`

**Examples:**
- k6 run --summary-trend-stats="avg,p(95),p(99)" script.js
- k6 run --out json=results.json script.js
- k6 run --out web-dashboard script.js

### cloud-integration
Run tests in k6 Cloud and inspect archives.

**Commands:**
- `k6 cloud run script.js`
- `k6 run --out cloud script.js`
- `k6 archive script.js`
- `k6 inspect script.js`
- `k6 cloud start --name "weekly capacity" script.js`

**Examples:**
- k6 cloud run script.js
- k6 archive script.js
- k6 inspect script.js
