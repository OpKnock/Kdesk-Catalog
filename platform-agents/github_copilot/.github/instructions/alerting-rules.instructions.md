---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Authors and tests Prometheus alerting rules and Alertmanager config: rule files, promtool validation, unit tests, silences, and the HTTP API.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `promtool check rules alerting-rules.yml`, `amtool check-config /etc/alertmanager/alertmanager.yml`
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

# Alerting Rules

## What this skill does

Authors and operates Prometheus alerting: rule files, promtool validation and unit tests, Alertmanager routing and silences, and alert state queries via the HTTP API.

## When to use

- Creating an alert for a new SLO or error condition
- Debugging an alert that fires (or fails to fire)
- Managing an outage via silences without stopping metrics collection

## Real commands

```bash
# Validate rules
promtool check rules alerts.yml

# Unit-test rule evaluation
promtool test rules tests.yml

# Inspect live alert state
curl -s 'http://localhost:9090/api/v1/rules?type=alert' | jq '.data.groups[].rules[] | {name,state}'

# Alertmanager
amtool check-config alertmanager.yml
amtool alert list
amtool silence add --expires=2h --author=oncall 'severity="critical"'
```

## Rules file

```yaml
groups:
- name: api
  rules:
  - alert: APIHighErrorRate
    expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "API 5xx rate above 5%"
```

## Unit test

```yaml
rule_files: [alerts.yml]
evaluation_interval: 1m
tests:
- interval: 1m
  input_series:
  - series: 'http_requests_total{status="500"}'
    values: '0+10x10'
  alert_rule_test:
  - eval_time: 10m
    alertname: APIHighErrorRate
```

## Testing

- Run `promtool check rules` in CI before merge
- Write promtool test rules cases for fire/no-fire thresholds

## Best practices

- Prefer SLO burn-rate alerts over raw thresholds
- Every alert needs a runbook URL in annotations
- Use `for:` clauses to avoid flapping

## Capabilities

### rules-authoring
Author Prometheus alerting/recording rules and validate them.

**Parameters:**
- `rules_file` (string): Path to the alerting rules YAML
- `test_file` (string): Path to promtool unit test YAML
- `query` (string): PromQL expression to evaluate

**Commands:**
- `promtool check rules alerting-rules.yml`
- `promtool test rules rules.test.yml`
- `promtool query instant 'up'`
- `promtool query range 'http_requests_total[5m]'`
- `curl 'http://localhost:9090/api/v1/rules?type=alert'`

**Examples:**
- promtool check rules /etc/prometheus/alerts.yml
- promtool test rules unit-tests.yml
- curl -s 'http://localhost:9090/api/v1/rules' | jq '.data.groups[].rules[] | {name, state}'

### alertmanager
Configure Alertmanager routing, manage silences, and inspect the API.

**Parameters:**
- `expires` (string): Silence duration, e.g. 1h
- `author` (string): Silence creator name
- `matchers` (string): Label matchers like severity="critical"

**Commands:**
- `amtool check-config /etc/alertmanager/alertmanager.yml`
- `amtool alert list`
- `amtool silence add --expires=1h 'severity="critical"'`
- `amtool silence list`
- `curl -X POST http://localhost:9093/api/v2/silences -d @silence.json`

**Examples:**
- amtool check-config /etc/alertmanager/alertmanager.yml
- amtool silence add --author=oncall --comment="draining node" 'instance="node1"'
- curl -X GET http://localhost:9093/api/v2/alerts | jq '.[].labels.alertname'

## References
- [Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [promtool](https://prometheus.io/docs/prometheus/latest/command-line/promtool/)
- [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
