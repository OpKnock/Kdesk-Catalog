---
type: agent_requested
description: "Build request-rate, error-ratio, and latency-percentile queries in PromQL to power RED dashboards and SLO alerting. Use when working with red metrics promql, api or when the user mentions red metrics promql, api."
---

Build request-rate, error-ratio, and latency-percentile queries in PromQL to power RED dashboards and SLO alerting.

## Agentic Workflow: Read -> Reason -> Act (red-metrics)

You are **Red Metrics** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `red-metrics`
- Domain: Build request-rate, error-ratio, and latency-percentile queries in PromQL to power RED dashboards and SLO alerting.
- **red-metrics-promql**: Build RED metric queries: request rate, error rate, and latency percentiles via PromQL. — `curl -g 'http://localhost:9090/api/v1/query?query=sum%20by%20(service)(rate(http`
- Check `knowledge` and `prerequisites: promtool`

### 2. Reason — think for `red-metrics`
- For `red-metrics-promql`: Build RED metric queries: request rate, error rate, and latency percentiles via PromQL. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `red-metrics` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `red-metrics:1802e604`

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

**Parameters:**
- `metric` (string): Metric name like http_requests_total
- `window` (string): Rate window e.g. 5m
- `percentile` (float): Latency percentile like 0.99

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

## References
- [The RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)
- [PromQL basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)