---
name: "artillery-mode"
description: "Load-tests APIs and WebSockets with Artillery v2: quick-mode runs, YAML scenarios, phases, assertions, and HTML reports. Use when working with quick mode, scenario tests, api or when the user mentions quick mode, scenario tests, api."
type: knowledge
triggers: ["artillery-mode", "quick-mode", "scenario-tests"]
---

Load-tests APIs and WebSockets with Artillery v2: quick-mode runs, YAML scenarios, phases, assertions, and HTML reports.

## Agentic Workflow: Read -> Reason -> Act (artillery-mode)

You are **Artillery Mode** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `artillery-mode`
- Domain: Load-tests APIs and WebSockets with Artillery v2: quick-mode runs, YAML scenarios, phases, assertions, and HTML reports.
- **quick-mode**: Run instant load tests without config files. — `npx artillery quick -d 60 -r 20 http://localhost:3000/api/users`
- **scenario-tests**: Write multi-step YAML scenarios with phases, hooks, and assertions. — `npx artillery run load-test.yml`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `artillery-mode`
- For `quick-mode`: Run instant load tests without config files. — decide which checks to run
- For `scenario-tests`: Write multi-step YAML scenarios with phases, hooks, and assertions. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `artillery-mode` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `artillery-mode:27a05c32`

# Artillery v2

## What this skill does

Load-tests APIs with Artillery: instant quick runs for smoke tests, YAML scenarios for realistic flows, phased load ramping, response assertions, and HTML report generation.

## When to use

- Verifying an endpoint's capacity before launch
- Catching latency regressions under load
- Reproducing a production spike pattern locally

## Real commands

```bash
# Quick smoke test: 60s at 20 RPS
npx artillery quick -d 60 -r 20 http://localhost:3000/api/users

# POST with body
npx artillery quick -d 30 -r 10 -m POST -b '{"name":"test"}' -H "Content-Type: application/json" http://localhost:3000/api/users

# Scenario test
npx artillery run load-test.yml

# Save + render report
npx artillery run --output report.json load-test.yml
npx artillery report report.json
```

## Scenario config

```yaml
config:
  target: http://localhost:3000
  phases:
    - duration: 60
      arrivalRate: 10
      rampTo: 50
    - duration: 120
      arrivalRate: 50
scenarios:
  - name: fetch users
    flow:
      - get:
          url: /api/users
          expect:
            statusCode: 200
```

## Testing

- Compare p99 latency against an SLO, not just the average
- Run 2-3 minutes of steady load before judging capacity

## Best practices

- Start with quick smoke tests, then formalize scenarios
- Assert statusCode and JSON bodies to fail on wrong responses
- Save raw JSON results as CI artifacts

## Capabilities

### quick-mode
Run instant load tests without config files.

**Parameters:**
- `duration` (number): Test duration in seconds (-d)
- `rate` (number): Requests per second (-r)
- `method` (string): HTTP method, e.g. GET/POST

**Commands:**
- `npx artillery quick -d 60 -r 20 http://localhost:3000/api/users`
- `npx artillery quick -d 30 -r 10 -m POST -b '{"name":"test"}' http://localhost:3000/api/users`
- `npx artillery quick --insecure https://staging.your-app.test/api`
- `npx artillery quick -d 60 -r 50 http://localhost:3000 -H "Authorization: Bearer $TOKEN"`

**Examples:**
- npx artillery quick -d 60 -r 20 http://localhost:3000/api/users
- npx artillery quick -d 30 -r 10 -m POST -b '{"name":"test"}' -H "Content-Type: application/json" http://localhost:3000/api/users
- npx artillery quick -d 120 -r 100 --output report.json http://localhost:3000

### scenario-tests
Write multi-step YAML scenarios with phases, hooks, and assertions.

**Parameters:**
- `environment` (string): Environment name from config (-e)
- `output` (string): JSON results output path
- `report` (string): Input JSON to render an HTML report

**Commands:**
- `npx artillery run load-test.yml`
- `npx artillery run --output report.json load-test.yml`
- `npx artillery report report.json`
- `npx artillery run -e staging load-test.yml`
- `npx artillery run --config base.yml --test-scenarios load-test.yml`

**Examples:**
- npx artillery run --output results.json load.yml && npx artillery report results.json
- npx artillery run -e production --quiet load.yml
- npx artillery run --snippet-mode load.yml

## References
- [Artillery Docs](https://www.artillery.io/docs)
- [Artillery Reference](https://www.artillery.io/docs/reference)
- [Getting Started](https://www.artillery.io/docs/guides/getting-started/installing-artillery)
