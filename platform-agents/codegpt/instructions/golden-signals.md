# Golden Signals

Query the four it from Prometheus and set up alerting. them from Prometheus metrics and wire dashboards and alerts.'

## Instructions

# Golden Signals

## What this skill does

The four golden signals are the minimum set of metrics to understand user-facing health: latency (time to serve), traffic (request rate), errors (failure rate), and saturation (how full the service is).

## When to use

- Building the first monitoring dashboard for a service
- Deciding what to alert on before adding noise
- Reviewing whether existing metrics cover all four signals

## Real commands

```bash
# 1. Latency: p99 request duration
curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq '.data.result[0].value[1]'

# 2. Traffic: requests per second
curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total[5m]))' | jq '.data.result[0].value[1]'

# 3. Errors: share of 5xx
curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))' | jq '.data.result[0].value[1]'

# 4. Saturation: CPU utilization
curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=rate(process_cpu_seconds_total[1m]) * 100' | jq '.data.result[0].value[1]'

# Validate alert rules
promtool check rules golden-signals.rules.yml
```

## Alert rules example

```yaml
groups:
  - name: golden
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
        for: 10m
      - alert: HighErrorRate
        expr: sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
```

## Dashboard layout

- Row 1: p50/p99 latency lines
- Row 2: request rate (by code class)
- Row 3: error ratio + count
- Row 4: CPU, memory, queue depth

## Best practices

- Measure latency in percentiles, never averages.
- Alert on error ratio, not raw error counts (traffic changes skew them).
- Add queue depth and CPU as saturation proxies when no direct metric exists.
- Attach each alert to a runbook; a signal without a response path is noise.
- Review the four signals before adding any other metric to dashboards.

## Capabilities

### golden-signals
Query the four golden signals from Prometheus and set up alerting.

**Commands:**
- `curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq '.data.result[0].value[1]'`
- `curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total[5m]))' | jq '.data.result[0].value[1]'`
- `curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))' | jq '.data.result[0].value[1]'`
- `curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=rate(process_cpu_seconds_total[1m]) * 100' | jq '.data.result[0].value[1]'`
- `promtool check rules golden-signals.rules.yml`

**Examples:**
- curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq '.data.result[0].value[1]'
- curl -s 'http://prometheus:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))' | jq '.data.result[0].value[1]'
- promtool check rules golden-signals.rules.yml
