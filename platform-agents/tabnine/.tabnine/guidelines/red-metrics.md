# Red Metrics

Build request-rate, error-ratio, and latency-percentile queries in PromQL to power RED dashboards and SLO alerting.

## Instructions

# RED Metrics

RED (Rate, Errors, Duration) is the standard health model for request-driven services.

## What this skill does

- Queries request rate, error rate and latency percentiles
- Builds dashboards and alerts from RED queries

## When to use

- Service health dashboards
- SLO alerting on request health

## Real commands

```bash
# Rate: requests per second
curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total%5B5m%5D))'
promtool query instant 'sum by (service) (rate(http_requests_total[5m]))' --url http://localhost:9090

# Errors: 5xx share
curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total%7Bstatus%3D~%225..%22%7D%5B5m%5D))%20%2F%20sum(rate(http_requests_total%5B5m%5D))'

# Duration: p99 latency
curl -g 'http://localhost:9090/api/v1/query?query=histogram_quantile(0.99%2C%20sum%20by%20(le)(rate(http_request_duration_seconds_bucket%5B5m%5D)))'
```

## Alert rule

```yaml
- record: service:error_ratio:rate5m
  expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
- alert: HighErrorRatio
  expr: service:error_ratio:rate5m > 0.05
  for: 5m
```

## Best practices

- Instrument each service with the same counter/histogram names
- Alert on error ratio, not raw error counts
- Use p95/p99 to catch tail latency

## Capabilities

### red-metrics-promql
Build RED metric queries: request rate, error rate, and latency percentiles via PromQL.

**Commands:**
- `curl -g 'http://localhost:9090/api/v1/query?query=sum%20by%20(service)(rate(http_requests_total%5B5m%5D))'`
- `curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total%7Bstatus%3D~%225..%22%7D%5B5m%5D))%20%2F%20sum(rate(http_requests_total%5B5m%5D))'`
- `curl -g 'http://localhost:9090/api/v1/query?query=histogram_quantile(0.99%2C%20sum%20by%20(le)(rate(http_request_duration_seconds_bucket%5B5m%5D)))'`
- `promtool query instant 'sum(rate(http_requests_total[5m]))' --url http://localhost:9090`
- `curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total%7Bstatus%3D~%222..%22%7D%5B5m%5D))'`

**Examples:**
- curl -g 'http://localhost:9090/api/v1/query?query=histogram_quantile(0.99,sum%20by%20(le)(rate(http_request_duration_seconds_bucket[5m])))' | jq '.data.result[0].value'
- promtool query instant 'sum by (service) (rate(http_requests_total[5m]))' --url http://localhost:9090
- curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total[5m]))'