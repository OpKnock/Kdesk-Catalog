---
trigger: glob
description: "Load-tests HTTP, WebSocket, and gRPC services with Artillery scripts, scenarios, and HTML reports. Use when working with artillery load tests, reporting, scenario design, testing or when the user mentions artillery load tests, reporting, scenario design, testing."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Load-tests HTTP, WebSocket, and gRPC services with Artillery scripts, scenarios, and HTML reports.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx artillery quick --count 100 -n 20 http://localhost:8080/`, `npx artillery report report.json`
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

# Artillery

Load and performance testing for HTTP, WebSocket, and gRPC.

## What This Skill Does

- Runs quick ad-hoc load tests from the CLI
- Executes scripted scenarios with phases and arrival rates
- Uses CSV payloads for realistic user data
- Generates HTML reports with latency percentiles

## When to Use

- Capacity checks before releases
- SLO validation under load
- Testing WebSocket and streaming endpoints

## Real Commands

```bash
# Quick test
npx artillery quick --count 100 -n 20 https://api.example.com/v1/users

# Scripted run
npx artillery run load-test.yml
npx artillery run --environment staging load-test.yml

# Reports
npx artillery run -o report.json load-test.yml
npx artillery report --output perf-report.html report.json

# Payloads
npx artillery run --payload users.csv scenarios.yml
```

## Sample Script

```yaml
config:
  target: https://api.example.com
  phases:
    - duration: 60
      arrivalRate: 10
      rampTo: 50
scenarios:
  - name: browse catalog
    flow:
      - get:
          url: /v1/products
      - think: 2
      - post:
          url: /v1/cart
          json: { productId: "{{ $randomNumber(1, 100) }}" }
```

## Best Practices

- Ramp arrival rate gradually; avoid instant max load
- Test realistic user flows, not just one endpoint
- Check percentiles (p95/p99) not just averages
- Run against staging with production-like data volumes
- Keep baseline reports to compare regressions

## Capabilities

### artillery-load-tests
Quick and scripted load tests with virtual users.

**Parameters:**
- `script` (string): YAML test script path
- `environment` (string): Named environment from config
- `count` (number): Virtual users for quick mode

**Commands:**
- `npx artillery quick --count 100 -n 20 http://localhost:8080/v1/users`
- `npx artillery run load-test.yml`
- `npx artillery run --environment staging load-test.yml`
- `npx artillery run -o report.json load-test.yml`
- `npx artillery run --record load-test.yml`

**Examples:**
- npx artillery quick --count 100 -n 20 http://localhost:8080/v1/users
- npx artillery run load-test.yml
- npx artillery run -o report.json load-test.yml

### reporting
Generate and inspect load-test reports.

**Parameters:**
- `input` (string): JSON results file
- `output` (string): HTML report output path

**Commands:**
- `npx artillery report report.json`
- `npx artillery report --output perf-report.html report.json`
- `npx artillery run --output report.json load-test.yml && npx artillery report report.json`

**Examples:**
- npx artillery report report.json
- npx artillery report --output perf-report.html report.json

### scenario-design
Design multi-step user flows with variables and phases.

**Parameters:**
- `payload` (string): CSV data file for virtual users
- `vars` (object): Inline variables override

**Commands:**
- `npx artillery run -e prod --vars '{"api": "/v1/orders"}' scenarios.yml`
- `npx artillery run --payload users.csv scenarios.yml`
- `npx artillery run --config env.yml scenarios.yml`

**Examples:**
- npx artillery run --payload users.csv scenarios.yml
- npx artillery run -e prod scenarios.yml

## References
- [Artillery Documentation](https://www.artillery.io/docs/)
- [Artillery Quick Reference](https://www.artillery.io/docs/reference/cli)
