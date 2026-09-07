---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Defines and measures service-level objectives with Prometheus SLIs, error-budget policies, and promtool rule validation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `promtool check rules slo-rules.yml`, `curl -s 'http://localhost:9090/api/v1/query?query=slo:availa`
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

# SLA / SLO / SLI

Turn availability and latency targets into measured, alertable SLOs.

## What This Skill Does

- Translates business targets into SLIs and SLO windows
- Writes Prometheus recording rules for ratios and error budgets
- Validates rules and tests with promtool
- Sets burn-rate alerts for fast page-on-alert behavior

## When to Use

- Defining service-level targets for a new service
- Auditing whether current SLIs are measured correctly
- Tuning alerts to fire on error-budget burn

## Real Commands

```bash
# Validate and test rules
promtool check rules slo-rules.yml
promtool test rules slo-tests.yml

# Check current SLO state
curl -s 'http://localhost:9090/api/v1/query?query=slo:availability_ratio:ratio_rate1h' | jq .
curl -s 'http://localhost:9090/api/v1/query?query=error_budget_burn' | jq .
```

## Sample SLO Rules

```yaml
groups:
  - name: slo-api-availability
    rules:
      - record: slo:http_errors:ratio_rate1h
        expr: |
          sum(rate(http_requests_total{job="api", status=~"5.."}[1h]))
          /
          sum(rate(http_requests_total{job="api"}[1h]))
      - record: error_budget_burn
        expr: slo:http_errors:ratio_rate1h / (1 - 0.995)
```

## Alert Levels

- 1x budget burn for 6h: ticket-worthy degradation
- 5x burn for 1h: page
- 15x burn for 10m: page immediately

## Best Practices

- Measure SLIs from the user's perspective (edge probes, not server logs)
- Keep windows to 28-30 days aligned with error-budget reviews
- Burn-rate alerts beat flat threshold alerts
- Document SLOs in the service catalog with the owning team
- Review budgets weekly; adjust targets only by policy, not silently

## Capabilities

### slo-rule-authoring
Author and validate Prometheus SLO rules and alerts.

**Parameters:**
- `ruleFile` (string): Prometheus rules file with SLO recording rules
- `query` (string): PromQL query to evaluate

**Commands:**
- `promtool check rules slo-rules.yml`
- `promtool test rules slo-tests.yml`
- `promtool query 'http_request_duration_seconds_bucket{le="0.5"}'`
- `promtool query range 'up' --start=2024-01-01T00:00:00Z --end=2024-01-02T00:00:00Z --step=1h`

**Examples:**
- promtool check rules slo-rules.yml
- promtool test rules slo-tests.yml
- promtool query 'sum(rate(http_requests_total{job="api"}[5m]))'

### slo-inspection
Query SLO state and error budgets from running Prometheus.

**Parameters:**
- `endpoint` (string): Prometheus API endpoint
- `metric` (string): SLO metric name to query

**Commands:**
- `curl -s 'http://localhost:9090/api/v1/query?query=slo:availability_ratio:ratio_rate1h' | jq .`
- `curl -s 'http://localhost:9090/api/v1/query?query=error_budget_burn' | jq .`
- `curl -s 'http://localhost:9090/api/v1/targets' | jq '.data.activeTargets | length'`
- `curl -s 'http://localhost:9090/api/v1/query_range?query=up&start=...&end=...&step=300' | jq .`

**Examples:**
- curl -s 'http://localhost:9090/api/v1/query?query=slo:availability_ratio:ratio_rate1h' | jq -r '.data.result[0].value[1]'
- curl -s 'http://localhost:9090/api/v1/query?query=error_budget_burn' | jq .

## References
- [Google SRE Workbook SLOs](https://sre.google/workbook/implementing-slos/)
- [Prometheus Recording Rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)
- [promtool Reference](https://prometheus.io/docs/prometheus/latest/command-line/promtool/)
