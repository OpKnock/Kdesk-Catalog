---
name: "k6"
description: "Load-tests APIs with k6 scripts, scenarios, thresholds, and Grafana Cloud reporting. Use when working with k6 runs, thresholds and reports, cloud integration, testing or when the user mentions k6 runs, thresholds and reports, cloud integration, testing."
---

Load-tests APIs with k6 scripts, scenarios, thresholds, and Grafana Cloud reporting.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `k6 run script.js`, `k6 run --summary-trend-stats="avg,p(95),p(99)" script.js`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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

**Parameters:**
- `vus` (number): Virtual users
- `duration` (string): Test duration, e.g. 30s, 2m
- `iterations` (number): Total iterations

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

**Parameters:**
- `out` (string): Output destination, e.g. json=file, cloud
- `tag` (string): Result tag, e.g. env=staging

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

**Parameters:**
- `name` (string): Cloud run name
- `out` (string): Result output destination: cloud or a local sink.

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

## References
- [k6 Documentation](https://grafana.com/docs/k6/)
- [k6 CLI Reference](https://grafana.com/docs/k6/using-k6/k6-options/reference/)
