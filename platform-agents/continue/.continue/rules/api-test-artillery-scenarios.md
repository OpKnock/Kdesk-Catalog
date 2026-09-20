---
name: "Api Test Artillery Scenarios"
description: "Runs performance and soak tests with Artillery: YAML scenarios, ramp loads, response time assertions, and HTML/JSON reports."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Api Test Artillery Scenarios

Runs performance and soak tests with Artillery: YAML scenarios, ramp loads, response time assertions, and HTML/JSON reports.

## Instructions

# API Test v4 - Performance Tests

Performance testing with Artillery.

## What This Skill Does
- Simulates user flows under load
- Ramps and soaks traffic
- Asserts latency thresholds

## When to Use
- Release performance validation
- Soak testing memory leaks
- Capacity estimation

## Real Commands

```bash
npx artillery quick --count 50 --num 20 https://api.example.com/users
npx artillery run config.yml
npx artillery run --output report.json config.yml
npx artillery report report.json
```

## Scenario Example

```yaml
config:
  target: https://api.example.com
  phases:
    - duration: 60
      arrivalRate: 10
      rampTo: 50
scenarios:
  - flow:
      - get:
          url: /api/users
      - think: 1
```

## Testing
- Run ramp and soak phases
- Assert p95 thresholds
- Export and compare reports


## Best Practices
- Separate soak from spike scenarios
- Monitor server metrics during runs
- Randomize data per iteration

## Capabilities

### artillery-scenarios
Define and run load test scenarios

**Commands:**
- `npx artillery run config.yml`
- `npx artillery quick --count 50 --num 20 http://localhost:8080/users`
- `npx artillery run --output report.json config.yml`
- `npx artillery run --environment staging config.yml`
- `npx artillery report report.json`

**Examples:**
- artillery quick runs ad-hoc load
- --output exports JSON results
- artillery report generates an HTML dashboard

### ramp-scenarios
Ramp virtual users over time

**Commands:**
- `npx artillery run --record --key $ARTILLERY_KEY soak.yml`
- `npx artillery run soak.yml`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:8080/health`

**Examples:**
- -cli --help
- -api --help