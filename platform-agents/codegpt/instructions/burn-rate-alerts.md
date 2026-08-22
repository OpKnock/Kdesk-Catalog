# Burn Rate Alerts

Designs SLO burn-rate alerts: multi-window burn rates, Prometheus rules, SLO windows, and alert fatigue control.

## Instructions

# Burn-Rate Alerts

## What this skill does

Designs SLO burn-rate alerts: computing error rates and burn rates with PromQL, authoring multi-window alert rules (e.g. 14.4x/5m, 6x/30m, 1x/6h), validating with promtool, and tracking budget consumption.

## When to use

- Replacing threshold alerts with SLO-based paging
- Answering 'how fast are we burning budget?'
- Reducing alert fatigue

## Real commands

```bash
# Error rate over 5m
promtool query instant 'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))'

# Availability over 1h
promtool query instant '1 - (sum(rate(http_requests_total{status=~"5.."}[1h])) / sum(rate(http_requests_total[1h])))'

# 30-day availability
curl -s 'http://localhost:9090/api/v1/query?query=(1%20-%20sum(rate(http_requests_total%7Bstatus%3D~%222..%22%7D%5B30d%5D))%20/%20sum(rate(http_requests_total%5B30d%5D)))' | jq -r '.data.result[0].value[1]'

# Validate rules
promtool check rules burn-rate.yml
promtool test rules burn-rate-test.yml
```

## Rule design (99% SLO)

- Page: burn rate >= 14.4 over 5m (2h to exhaust budget)
- Page: burn rate >= 6 over 30m (5h to exhaust)
- Ticket: burn rate >= 1 over 6h (3 days to exhaust)

## Testing

- Unit-test each window's firing conditions with promtool test rules
- Confirm short-burst errors do not page (window guards)

## Best practices

- Use two windows per severity (fast/slow)
- Compute burn rate = error_rate / (1 - SLO)
- Track remaining budget monthly and review

## Capabilities

### slo-calculation
Compute error budget and burn rates.

**Commands:**
- `promtool query instant 'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))'`
- `promtool query instant '1 - (sum(rate(http_requests_total{status=~"2.."}[1h])) / sum(rate(http_requests_total[1h])))'`
- `curl -s 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total%5B5m%5D))' | jq '.data.result'`
- `python -c "print('burn_rate = error_rate / error_budget_share')"`

**Examples:**
- promtool query instant 'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))'
- curl -s 'http://localhost:9090/api/v1/query?query=(1%20-%20sum(rate(http_requests_total%7Bstatus%3D~%222..%22%7D%5B1h%5D))%20/%20sum(rate(http_requests_total%5B1h%5D)))' | jq .
- promtool query range 'sum(rate(http_requests_total[5m]))' --start=... --end=... --step=60

### multi-window-rules
Author multi-window, multi-burn-rate alert rules.

**Commands:**
- `promtool check rules burn-rate.yml`
- `promtool test rules burn-rate-test.yml`
- `curl -s 'http://localhost:9090/api/v1/rules?type=alert' | jq '.data.groups[].rules[] | {name,state}'`
- `amtool alert list`

**Examples:**
- promtool check rules /etc/prometheus/burn-rate.yml
- promtool test rules burn-rate-test.yml
- curl -s 'http://localhost:9090/api/v1/rules?type=alert' | jq -r '.data.groups[].rules[] | select(.state=="firing") | .name'

### budget-ops
Track error budget consumption.

**Commands:**
- `curl -s 'http://localhost:9090/api/v1/query?query=(1%20-%20sum(rate(http_requests_total%7Bstatus%3D~%222..%22%7D%5B30d%5D))%20/%20sum(rate(http_requests_total%5B30d%5D)))' | jq '.data.result[0].value[1]'`
- `promtool query instant 'error_rate_30d gt 0.01'`
- `curl -s 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total%5B30d%5D))' | jq .`

**Examples:**
- curl -s 'http://localhost:9090/api/v1/query?query=(1%20-%20sum(rate(http_requests_total%7Bstatus%3D~%222..%22%7D%5B30d%5D))%20/%20sum(rate(http_requests_total%5B30d%5D)))' | jq -r '.data.result[0].value[1]'
- promtool query instant 'error_budget_remaining = 1 - (1 - availability30d) / (1 - 0.99)'
- curl -s 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total%7Bstatus%3D~%225..%22%7D%5B30d%5D))%20/%20sum(rate(http_requests_total%5B30d%5D))' | jq .
