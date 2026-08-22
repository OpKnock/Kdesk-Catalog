---
name: "prometheus"
description: "Validate and test it configuration and rules. Write recording and alerting rules with tests. production monitoring.'"
---

# prometheus

Validate and test it configuration and rules. Write recording and alerting rules with tests. production monitoring.'

## Instructions

# Prometheus

Run Prometheus with validated configs and tested rules.

## When to Use

- Setting up scrape targets and retention
- Adding recording rules for expensive queries
- Alerting rules reviewed before deploy

## Validate everything

```bash
promtool check config prometheus.yml --lint=error
promtool check rules rules.yml --strict
```

## Recording rules

```yaml
groups:
  - name: api-usage
    interval: 1m
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))
```

Recording rules precompute heavy queries for dashboards.

## Alert rules

```yaml
groups:
  - name: availability
    rules:
      - alert: ApiDown
        expr: up{job="api"} == 0
        for: 2m
        labels: { severity: critical }
        annotations:
          summary: 'API {{ $labels.instance }} is down'
```

## Test rules

```yaml
rule_files:
  - rules.yml
evaluation_interval: 1m
tests:
  - interval: 1m
    input_series:
      - series: 'up{job="api"}'
        values: '0+0x30'
    alert_rule_test:
      - eval_time: 3m
        alertname: ApiDown
        exp_alerts: []
```

```bash
promtool test rules tests/rules_test.yml
```

## Live inspection

```bash
curl -s http://localhost:9090/api/v1/alerts | jq '.data.alerts[] | {alertname: .labels.alertname, state}'
curl -s http://localhost:9090/api/v1/rules | jq '.data.groups | length'
```

## Best practices

- Add `for:` durations to suppress transient alerts.
- Cap alert labels; too many produce notification storms.
- Test every new rule before merge.
- Keep retention and storage sizing reviewed quarterly.

## Testing

```bash
promtool check config prometheus.yml
promtool test rules tests/rules_test.yml
```

Both run in CI on every config change.

## Capabilities

### promtool
Validate and test Prometheus configuration and rules.

**Commands:**
- `promtool check config prometheus.yml`
- `promtool check rules rules.yml`
- `promtool test rules test.yml`
- `promtool check metrics /tmp/metrics.txt`
- `promtool config routes prometheus.yml`

**Examples:**
- promtool check config prometheus.yml --lint=error
- promtool test rules tests/rules_test.yml
- promtool check rules rules/*.yml --strict

### rules
Write recording and alerting rules with tests.

**Commands:**
- `curl -s http://localhost:9090/api/v1/rules | jq '.data.groups[] | {name, rules: [.rules[].name]}'`
- `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up'`
- `curl -s http://localhost:9090/api/v1/alerts | jq '.data.alerts[] | {labels: .labels.alertname, state}'`
- `promtool tsdb list /var/lib/prometheus`
- `curl -s http://localhost:9090/api/v1/status/tsdb | jq '.data'`

**Examples:**
- curl -s http://localhost:9090/api/v1/rules | jq '.data.groups | length'
- curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=rate(http_requests_total[5m])'
- promtool tsdb list /var/lib/prometheus | head
