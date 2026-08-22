---
type: agent_requested
description: "Web performance analysis: Lighthouse audits, load testing, and request timing measurements."
---

# performance

Web performance analysis: Lighthouse audits, load testing, and request timing measurements.

## Instructions

# Performance

Measures and diagnoses web performance: lab audits (Lighthouse), load tests, and
raw request timing.

## When to Use

- Auditing Core Web Vitals (LCP, INP, CLS)
- Comparing page speed before/after a change
- Capacity testing an API or web server

## Real Commands

```bash
# Lighthouse JSON audit
npx lighthouse https://example.com --output=json --output-path=./lh.json

# HTML report for sharing
npx lighthouse https://example.com --output=html --output-path=./lh.html

# Performance-only with a budget
npx lighthouse https://example.com --only-categories=performance --budget-path=budget.json

# Quick TTFB measurement
curl -o /dev/null -s -w '%{time_total}s ttfb=%{time_starttransfer}s
' https://example.com

# Load test with wrk
wrk -t4 -c100 -d30s http://localhost:3000/ --latency

# Scripted load test with k6
k6 run load-test.js
```

## Budget Example (budget.json)

```json
{
  "timings": [{"metric": "lcp", "budget": 2500}],
  "resourceSizes": [{"resourceType": "script", "budget": 200}]
}
```

## k6 Script Example

```js
import http from 'k6/http';
import { check } from 'k6';

export const options = { vus: 50, duration: '60s' };

export default function () {
  const res = http.get('https://example.com/');
  check(res, { 'status 200': (r) => r.status === 200 });
}
```

## Best Practices

- Run Lighthouse on a fixed device profile (Moto G Power / slow 4G) for comparability
- Measure before and after; one-off numbers are noisy
- Use `wrk --latency` to see percentile tails, not just averages
- Combine lab (Lighthouse) and field (RUM) data for the full picture

## Example Response

Returns Lighthouse scores per category with the top 5 performance opportunities
(LCP, TBT, CLS), plus curl timing breakdown and load-test percentile latencies.

## Capabilities

### web-performance
Measure page performance with Lighthouse, curl timing, and load tests

**Commands:**
- `npx lighthouse http://localhost:8080 --output=json --output-path=./lh-report.json`
- `curl -o /dev/null -s -w 'total: %{time_total}s ttfb: %{time_starttransfer}s
' https://example.com`
- `npx lighthouse http://localhost:8080 --only-categories=performance --budget-path=budget.json`
- `wrk -t4 -c100 -d30s http://localhost:3000/`
- `k6 run load-test.js`

**Examples:**
- npx lighthouse http://localhost:8080 --chrome-flags='--headless' --output=html
- curl -w '%{http_code} %{time_total}' -o /dev/null http://localhost:8080/api/health
- wrk -t8 -c200 -d60s http://localhost:8080/api --latency