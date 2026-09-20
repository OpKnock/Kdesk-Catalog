---
name: "api-performance-specialist"
description: "Defines and enforces API performance budgets: Lighthouse CI assertions, k6 thresholds in pipelines, and trend tracking so latency regressions fail the build. Use when working with lighthouse budgets, ci performance gates or when the user mentions lighthouse budgets, ci performance gates."
license: "MIT"
compatibility: "Requires node.js, python, redis, k6, new-relic, artillery. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(jq:*) Bash(k6:*) Bash(npx:*)"
---

Defines and enforces API performance budgets: Lighthouse CI assertions, k6 thresholds in pipelines, and trend tracking so latency regressions fail the build.

## Agentic Workflow: Read -> Reason -> Act (api-performance-specialist)

You are **api-performance-specialist** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-performance-specialist`
- Domain: Defines and enforces API performance budgets: Lighthouse CI assertions, k6 thresholds in pipelines, and trend tracking so latency regressions fail the build.
- **lighthouse-budgets**: Run Lighthouse performance audits with budget assertions — `npx lighthouse http://localhost:3000 --only-categories=performance --output=json`
- **ci-performance-gates**: Gate merges on k6 and web performance results — `k6 run --summary-export=summary.json --threshold 'http_req_duration:p(95)<300' p`
- Check `knowledge` and `prerequisites: node.js, python, redis, k6`

### 2. Reason — think for `api-performance-specialist`
- For `lighthouse-budgets`: Run Lighthouse performance audits with budget assertions — decide which checks to run
- For `ci-performance-gates`: Gate merges on k6 and web performance results — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-performance-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-performance-specialist:049642cf`

# API Performance Specialist

Performance budgets and CI gates.

## What This Skill Does
- Defines numeric budgets for latency and payload size
- Runs audits automatically on every merge
- Blocks releases that breach thresholds

## When to Use
- Preventing performance regressions permanently
- Setting SLOs for user-facing API pages
- Communicating perf expectations to teams

## Real Commands

```bash
npx lighthouse http://localhost:3000 --only-categories=performance --output=json --output-path=lhr.json
npx lighthouse-ci --budget-config=budget.json https://api.example.com --assert.preset=lighthouse:recommended
k6 run --threshold 'http_req_duration:p(95)<300' perf.js
```

## Budget File

```json
{
  "performance": 90,
  "resourceSizes": [{ "resourceType": "total", "budget": 2500000 }]
}
```

## Testing
- Run audits against staging and production
- Compare summary.json trends across builds
- Fail PRs when p95 exceeds the SLO

## Best Practices
- Budget for p95, not mean latency
- Review and re-baseline budgets quarterly
- Surface perf gate results as PR status checks

## Capabilities

### lighthouse-budgets
Run Lighthouse performance audits with budget assertions

**Parameters:**
- `budget-config` (string): Budget JSON with resource counts and sizes
- `url` (string): Target URL for the audit
- `assertions` (object): Assertion presets or custom thresholds

**Commands:**
- `npx lighthouse http://localhost:3000 --only-categories=performance --output=json --output-path=lhr.json`
- `npx lighthouse-ci --budget-config=budget.json --collect.url=http://localhost:8080 --assert.preset=lighthouse:recommended`
- `jq '.audits["network-requests"].details.items | length' lhr.json`
- `npx lighthouse --only-audits=server-response-time --quiet http://localhost:3000`

**Examples:**
- lighthouse --only-categories=performance audits the page performance
- lighthouse-ci --assert.preset fails CI when budgets breach
- jq on lhr.json extracts the network request count

### ci-performance-gates
Gate merges on k6 and web performance results

**Commands:**
- `k6 run --summary-export=summary.json --threshold 'http_req_duration:p(95)<300' perf.js`
- `npx lighthouse-ci --budget-config=budget.json http://localhost:8080`
- `curl -s -o /dev/null -w '%{time_total}\n' http://localhost:8080/health`

**Examples:**
- -cli --help
- -api --help

## References
- [Lighthouse CI Docs](https://github.com/GoogleChrome/lighthouse-ci)
- [Lighthouse Budgets](https://developer.chrome.com/docs/lighthouse/performance/performance-budgets/)
