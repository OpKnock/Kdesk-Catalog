---
type: agent_requested
description: "Load-tests pagination endpoints with k6 and autocannon: deep-page queries, worst-case limits, cursor stress, and performance regression detection in CI. Use when working with pagination load tests, deep page analysis or when the user mentions pagination load tests, deep page analysis."
---

Load-tests pagination endpoints with k6 and autocannon: deep-page queries, worst-case limits, cursor stress, and performance regression detection in CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `k6 run pagination-test.js`, `k6 run --iterations 200 deep-page.js`
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

# API Pagination v5 - Performance

Load testing pagination endpoints.

## What This Skill Does
- Scripts realistic pagination walk scenarios in k6
- Benchmarks worst-case page sizes and deep pages
- Sets thresholds to gate pagination regressions

## When to Use
- Before moving pagination to cursor mode
- Tuning page size defaults
- Catching O(n) OFFSET degradation

## Real Commands

```bash
k6 run pagination-test.js
npx autocannon -c 10 -d 30 'http://localhost:3000/users?page=1&limit=100'
ab -n 2000 -c 50 'http://localhost:3000/users?limit=50'
```

## k6 Scenario

```js
import http from 'k6/http';
export const options = {
  thresholds: { http_req_duration: ['p(95)<250'] }
};
export default function () {
  const r = http.get('http://localhost:3000/users?page=1&limit=50');
  const next = r.json().next;
  if (next) http.get(next);
}
```

## Testing
- Compare p95 at page 1 vs page 500 to expose OFFSET cost
- Test limit at the configured maximum
- Break tests into categories: first page, middle page, last page

## Best Practices
- Keep thresholds aggressive on p95 not averages
- Run against a seeded dataset, not an empty table
- Assert page size caps prevent pathological queries

## Capabilities

### pagination-load-tests
Run load scenarios targeting pagination endpoints

**Parameters:**
- `vus` (integer): k6 virtual users
- `duration` (string): Test duration like 60s
- `limit` (integer): Page size under test

**Commands:**
- `k6 run pagination-test.js`
- `npx autocannon -c 10 -d 30 'http://localhost:3000/users?page=1&limit=100'`
- `ab -n 2000 -c 50 'http://localhost:3000/users?limit=50'`
- `k6 run --vus 20 --duration 60s --summary-export=summary.json pagination-test.js`
- `curl -s -o /dev/null -w '%{time_total} %{http_code}\n' 'http://localhost:3000/users?cursor=deep&limit=100'`

**Examples:**
- k6 run pagination-test.js exercises cursor walks in a loop
- autocannon -c 10 -d 30 floods the limit=100 endpoint
- ab -n 2000 -c 50 measures throughput with offsets

### deep-page-analysis
Detect O(n) degradation on deep pagination

**Commands:**
- `k6 run --iterations 200 deep-page.js`
- `curl -s 'http://localhost:3000/api/timing?page=1' | jq '.serverTimeMs'`
- `curl -s 'http://localhost:3000/api/timing?page=500' | jq '.serverTimeMs'`
- `npx autocannon -c 5 -d 20 'http://localhost:3000/users?page=500'`

**Examples:**
- -cli --help
- -api --help

## References
- [k6 Documentation](https://grafana.com/docs/k6/latest/)
- [autocannon](https://github.com/mcollina/autocannon)