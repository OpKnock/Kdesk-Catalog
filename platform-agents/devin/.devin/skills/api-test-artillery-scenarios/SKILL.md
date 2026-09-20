---
name: "api-test-artillery-scenarios"
description: "Runs performance and soak tests with Artillery: YAML scenarios, ramp loads, response time assertions, and HTML/JSON reports. Use when working with artillery scenarios, ramp scenarios or when the user mentions artillery scenarios, ramp scenarios."
license: "MIT"
compatibility: "Requires jest, pytest, postman, newman, supertest. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(npx:*)"
---

Runs performance and soak tests with Artillery: YAML scenarios, ramp loads, response time assertions, and HTML/JSON reports.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx artillery run config.yml`, `npx artillery run --record --key $ARTILLERY_KEY soak.yml`
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

**Parameters:**
- `config` (string): YAML test config
- `environment` (string): Environment profile
- `output` (string): Results file

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

## References
- [Artillery Docs](https://www.artillery.io/docs)
- [Artillery YAML Reference](https://www.artillery.io/docs/reference/test-script)
