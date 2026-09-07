Establish performance baselines: k6 load tests, thresholds, trend stats, and regression comparison.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `k6 run --vus 50 --duration 30s script.js`
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

**Parameters:**
- `vus` (integer): Number of virtual users
- `duration` (string): Test duration like 30s or 1m
- `script` (string): Path to the k6 test script

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

## References
- [k6 Documentation](https://grafana.com/docs/k6/latest/)
- [k6 Metrics Reference](https://grafana.com/docs/k6/latest/using-k6/metrics/)