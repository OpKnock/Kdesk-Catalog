---
trigger: glob
description: "Establish performance baselines: k6 load tests, thresholds, trend stats, and regression comparison."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Performance Baseline

Establish performance baselines: k6 load tests, thresholds, trend stats, and regression comparison.

## Instructions

# Performance Baselines

Baselines give you a number to compare against every release, catching regressions early.

## What this skill does

- Writes k6 scenarios with realistic load
- Sets thresholds that fail the build
- Stores results for comparison

## When to use

- Before big releases
- After infra changes (DB, caches, deploys)

## Real commands

```bash
# Run a load test
k6 run --vus 50 --duration 30s script.js

# Inspect script structure
k6 inspect script.js

# Custom stats
k6 run --summary-trend-stats="avg,p(95),p(99)" script.js

# Environment override
k6 run --env BASE_URL=https://staging.your-app.test script.js

# JSON output for comparison
k6 run --out json=results.json script.js
```

## Script with thresholds

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('http://localhost:8080/api/health');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Best practices

- Fix the baseline dataset and environment for comparability
- Compare p(95), not averages
- Run in CI with thresholds to gate releases

## Capabilities

### k6-baseline-testing
Write and run k6 load tests with thresholds, virtual users and summary statistics.

**Commands:**
- `k6 run --vus 50 --duration 30s script.js`
- `k6 inspect script.js`
- `k6 run --summary-trend-stats="avg,p(95),p(99)" script.js`
- `k6 run --env BASE_URL=https://staging.your-app.test script.js`
- `k6 run --out json=results.json script.js`

**Examples:**
- k6 run --vus 20 --duration 1m --summary-trend-stats='avg,p(90),p(95)' script.js
- k6 inspect script.js
- k6 run --out json=results.json --vus 100 --duration 2m script.js
