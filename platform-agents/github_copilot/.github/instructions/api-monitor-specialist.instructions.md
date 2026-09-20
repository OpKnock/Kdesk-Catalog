---
applyTo: "**/*.html **/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# api-monitor-specialist

Builds scheduled API monitoring with Postman collections and Newman: environment-driven runs, HTML/JSON reporters, iteration data, and CI-friendly exit codes.

## Instructions

# API Monitor Specialist

Scheduled API monitoring with Newman.

## What This Skill Does
- Executes Postman collections as health checks
- Reports results as JSON/HTML artifacts
- Fails CI builds when API checks fail

## When to Use
- Smoke-testing a deploy before traffic is cut over
- Continuous monitoring of critical endpoints
- Turning ad-hoc Postman collections into checks

## Real Commands

```bash
npm install -g newman newman-reporter-htmlextra
newman run postman_collection.json -e production.postman_environment.json -r cli,json \
  --reporter-json-export results.json
newman run collection.json -n 5 --timeout-request 10000
```

## Monitoring Structure
- Environments hold baseUrl and API keys per stage
- Assertions inside requests check status and body
- Folders group checks by domain (auth, billing, health)

## Testing
- Run with --iteration-data to simulate multiple tenants
- Use --timeout-request to catch hangs
- Parse results.json in CI to annotate pull requests

## Best Practices
- Keep collections in version control
- Store secrets in environments, never in collections
- Schedule via cron in CI for round-the-clock coverage

## Capabilities

### newman-runs
Run Postman collections as monitoring checks

**Commands:**
- `npm install -g newman newman-reporter-htmlextra`
- `newman run postman_collection.json -e production.postman_environment.json -r cli,json --reporter-json-export results.json`
- `newman run collection.json -n 5 --timeout-request 10000`
- `newman run collection.json --folder auth --iteration-data data.csv`
- `curl -s https://postman-echo.com/get -o /dev/null -w '%{http_code} %{time_total}s\n'`

**Examples:**
- newman run collection.json -e prod.json --reporters cli,htmlextra generates an HTML dashboard
- newman run collection.json -n 5 polls an endpoint five times for flakiness
- echo $? after newman reflects pass/fail for CI gates

### collection-export
Convert collections to OpenAPI for contract drift checks

**Commands:**
- `npx postman-to-openapi postman_collection.json -o openapi.yaml`
- `newman run openapi.yaml --reporters cli`
- `node -e "const c = require('./collection.json'); console.log(c.item.length)"`

**Examples:**
- -cli --help
- -api --help
