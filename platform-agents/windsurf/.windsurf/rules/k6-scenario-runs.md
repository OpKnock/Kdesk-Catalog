---
trigger: glob
description: "Advanced load testing with Grafana k6: scenario-based scripts, threshold gates, ramping VUs, and structured result export for CI analysis."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# K6 Scenario Runs

Advanced load testing with Grafana k6: scenario-based scripts, threshold gates, ramping VUs, and structured result export for CI analysis.

## Instructions

# k6 (Advanced)

Run scenario-driven load tests with Grafana k6 and gate releases on thresholds.

## What this skill does

- Runs k6 scripts with executors (ramping-vus, constant-arrival-rate, shared-iterations).
- Enforces threshold gates that fail the test run on SLO breaches.
- Exports JSON summaries for dashboards and archives for replay.

## When to use

- Pre-release capacity validation.
- SLO regression checks in CI (k6 run gates the pipeline).
- Spike/soak testing with scenario scheduling.

## Real commands

```bash
# Quick run
k6 run script.js

# Ramped run
k6 run --vus 50 --duration 1m script.js

# Environment override
k6 run -e BASE_URL=https://staging.example.com script.js

# Trend stats
k6 run --summary-trend-stats="avg,p(95),p(99)" script.js

# Inspect resolved options
k6 inspect script.js | jq .options

# Export summary + full JSON
k6 run --summary-export=summary.json script.js
k6 run --out json=results.json script.js
```

## Script example (ramping scenario)

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    ramping: {
      executor: 'ramping-vus',
      stages: [
        { duration: '30s', target: 20 },
        { duration: '1m', target: 100 },
        { duration: '30s', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<800'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(__ENV.BASE_URL + '/api/orders');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Testing

```bash
k6 run --vus 10 --iterations 20 script.js   # smoke check before the real run
```

## Best practices

- Set thresholds in the script so CI fails fast on regressions.
- Use --summary-export and commit the JSON for trend tracking.
- Always run a tiny smoke run before the full load to catch script errors.

## Capabilities

### scenario-runs
Run k6 scripts with scenarios, ramping profiles, and environment overrides.

**Commands:**
- `k6 run script.js`
- `k6 run --vus 50 --duration 1m script.js`
- `k6 run --scenario ramping -e BASE_URL=https://staging.your-app.test script.js`
- `k6 run --summary-trend-stats="avg,p(95),p(99),p(99.9)" script.js`
- `k6 inspect script.js`

**Examples:**
- k6 run --vus 50 --duration 1m script.js
- k6 run -e BASE_URL=https://staging.your-app.test --summary-trend-stats=p(95) script.js
- k6 inspect script.js | jq .options.scenarios

### export-archive
Export JSON summaries and archives for CI dashboards and later replay.

**Commands:**
- `k6 run --summary-export=summary.json script.js`
- `k6 archive script.js`
- `k6 run --iterations 100 --max-exported-metrics-to-keep=500 script.js`
- `k6 run --out json=results.json script.js`

**Examples:**
- k6 run --summary-export=summary.json script.js
- k6 archive script.js && k6 run archive.tar
- k6 run --out json=results.json script.js
