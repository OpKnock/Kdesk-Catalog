---
name: "red-metrics"
description: "Build request-rate, error-ratio, and latency-percentile queries in PromQL to power RED dashboards and SLO alerting. Use when working with red metrics promql, api or when the user mentions red metrics promql, api."
license: "MIT"
compatibility: "Requires promtool. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(promtool:*)"
---

Build request-rate, error-ratio, and latency-percentile queries in PromQL to power RED dashboards and SLO alerting.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -g 'http://localhost:9090/api/v1/query?query=sum%20by%2`
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
