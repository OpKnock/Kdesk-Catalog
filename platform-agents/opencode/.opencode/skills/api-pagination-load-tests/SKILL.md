---
name: "api-pagination-load-tests"
description: "Load-tests pagination endpoints with k6 and autocannon: deep-page queries, worst-case limits, cursor stress, and performance regression detection in CI. Use when working with pagination load tests, deep page analysis or when the user mentions pagination load tests, deep page analysis."
---

Load-tests pagination endpoints with k6 and autocannon: deep-page queries, worst-case limits, cursor stress, and performance regression detection in CI.

## Agentic Workflow: Read -> Reason -> Act (api-pagination-load-tests)

You are **Api Pagination Load Tests** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-pagination-load-tests`
- Domain: Load-tests pagination endpoints with k6 and autocannon: deep-page queries, worst-case limits, cursor stress, and performance regression detection in CI.
- **pagination-load-tests**: Run load scenarios targeting pagination endpoints — `k6 run pagination-test.js`
- **deep-page-analysis**: Detect O(n) degradation on deep pagination — `k6 run --iterations 200 deep-page.js`
- Check `knowledge` and `prerequisites: node.js, python, postgresql`

### 2. Reason — think for `api-pagination-load-tests`
- For `pagination-load-tests`: Run load scenarios targeting pagination endpoints — decide which checks to run
- For `deep-page-analysis`: Detect O(n) degradation on deep pagination — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-pagination-load-tests` tools
- Tools: `Glob`, `Grep`, `Read`, `K6`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-pagination-load-tests:73726b9b`

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
