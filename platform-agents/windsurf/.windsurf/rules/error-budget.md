---
trigger: glob
description: "SLO and error budget management: compute error budgets from Prometheus metrics, track burn rates, and trigger alerts when budgets deplete."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Error Budget

SLO and error budget management: compute error budgets from Prometheus metrics, track burn rates, and trigger alerts when budgets deplete.

## Instructions

# Error Budget

## What this skill does

An error budget is the allowed failure over an SLO period: at 99.9% availability over 30 days, 43 minutes of error is the budget. This skill computes SLIs from Prometheus, tracks burn, and wires alerts.

## When to use

- Setting up SLOs for a new service
- Deciding whether a release can proceed (budget check)
- Investigating which window consumed the budget

## Real commands

```bash
# Request rate (RPS)
curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total{job="api"}[5m]))' | jq '.data.result[0].value'

# Availability SLI (percent of good requests)
curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=(1 - sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100' | jq '.data.result[0].value[1]'

# Latency SLI (P95)
curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq

# Validate alert rules
promtool check rules prometheus/rules.yml
promtool test rules test.yml
```

## Burn rate example (Prometheus rule)

```yaml
groups:
  - name: slo
    rules:
      - alert: ErrorBudgetBurnRate
        expr: (1 - sum(rate(http_requests_total{code=~"5.."}[1h])) / sum(rate(http_requests_total[1h]))) < 0.99
        for: 15m
        labels:
          severity: page
```

## Budget math

- 99.9% over 30 days = 43m 12s budget
- 99.95% over 30 days = 21m 36s
- Monthly budget seconds = (1 - target) * days * 86400

## Best practices

- Alert on burn rate (budget depletion speed), not raw error count.
- Use a 1h fast-burn and 6h slow-burn alert pair.
- Review budget consumption weekly in the on-call report.
- Freeze risky releases when burn crosses ~15% of the monthly budget.

## Capabilities

### budget-calculations
Query availability and latency SLIs, compute burn, and alert on budget depletion.

**Commands:**
- `curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total{job="api"}[5m]))' | jq '.data.result[0].value'`
- `curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=(1 - sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100' | jq '.data.result[0].value[1]'`
- `curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq`
- `promtool check rules prometheus/rules.yml`
- `promtool test rules test.yml`

**Examples:**
- curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=(1 - sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100' | jq '.data.result[0].value[1]'
- curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq
- promtool check rules prometheus/rules.yml
