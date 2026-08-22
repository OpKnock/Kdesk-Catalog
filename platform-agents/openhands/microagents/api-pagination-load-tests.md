---
name: "api-pagination-load-tests"
description: "Load-tests pagination endpoints with k6 and autocannon: deep-page queries, worst-case limits, cursor stress, and performance regression detection in CI."
type: knowledge
triggers: ["api-pagination-load-tests", "pagination-load-tests", "deep-page-analysis"]
---

# Api Pagination Load Tests

Load-tests pagination endpoints with k6 and autocannon: deep-page queries, worst-case limits, cursor stress, and performance regression detection in CI.

## Instructions

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
