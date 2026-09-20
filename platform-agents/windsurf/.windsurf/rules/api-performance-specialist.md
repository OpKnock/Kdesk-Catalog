---
trigger: glob
description: "Defines and enforces API performance budgets: Lighthouse CI assertions, k6 thresholds in pipelines, and trend tracking so latency regressions fail the build. Use when working with lighthouse budgets, ci performance gates or when the user mentions lighthouse budgets, ci performance gates."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

Defines and enforces API performance budgets: Lighthouse CI assertions, k6 thresholds in pipelines, and trend tracking so latency regressions fail the build.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx lighthouse http://localhost:3000 --only-categories=perfo`, `k6 run --summary-export=summary.json --threshold 'http_req_d`
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
