---
name: "artillery"
description: "Load-tests HTTP, WebSocket, and gRPC services with Artillery scripts, scenarios, and HTML reports."
---

# artillery

Load-tests HTTP, WebSocket, and gRPC services with Artillery scripts, scenarios, and HTML reports.

## Instructions

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

**Commands:**
- `npx artillery report report.json`
- `npx artillery report --output perf-report.html report.json`
- `npx artillery run --output report.json load-test.yml && npx artillery report report.json`

**Examples:**
- npx artillery report report.json
- npx artillery report --output perf-report.html report.json

### scenario-design
Design multi-step user flows with variables and phases.

**Commands:**
- `npx artillery run -e prod --vars '{"api": "/v1/orders"}' scenarios.yml`
- `npx artillery run --payload users.csv scenarios.yml`
- `npx artillery run --config env.yml scenarios.yml`

**Examples:**
- npx artillery run --payload users.csv scenarios.yml
- npx artillery run -e prod scenarios.yml
