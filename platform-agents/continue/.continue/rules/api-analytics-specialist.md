---
name: "api-analytics-specialist"
description: "Deep API analytics: PromQL expertise, query range analysis, log-based analytics with Elasticsearch, and correlating metrics with deployments. Use when working with analytics deep or when the user mentions analytics deep."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Deep API analytics: PromQL expertise, query range analysis, log-based analytics with Elasticsearch, and correlating metrics with deployments.

## Agentic Workflow: Read -> Reason -> Act (api-analytics-specialist)

You are **api-analytics-specialist** (sre) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `api-analytics-specialist`
- Domain: Deep API analytics: PromQL expertise, query range analysis, log-based analytics with Elasticsearch, and correlating metrics with deployments.
- **analytics-deep**: Advanced analytics queries and log correlation — `curl -G 'http://localhost:9090/api/v1/query_range' --data-urlencode 'query=rate(`
- Check `knowledge` and `prerequisites: prometheus, grafana, elasticsearch`

### 2. Reason — think for `api-analytics-specialist`
- For `analytics-deep`: Advanced analytics queries and log correlation — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-analytics-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-analytics-specialist:c6c39cd9`

# API Analytics Specialist

## What this skill does
Expert-level API analytics: range queries, alert rules, log-based analysis with Elasticsearch, and correlating metric anomalies with deployments and releases.

## When to use
- Investigating performance regressions
- Building alert rules that don't false-positive
- Correlating logs and metrics

## Real commands
```bash
# Range query over one hour
curl -G 'http://localhost:9090/api/v1/query_range' \
  --data-urlencode 'query=rate(http_requests_total[5m])' \
  --data-urlencode 'start=2024-06-01T00:00:00Z' \
  --data-urlencode 'end=2024-06-01T01:00:00Z' \
  --data-urlencode 'step=60' | jq '.data.result[0].values | length'

# Same via promtool
promtool query range 'rate(http_requests_total[1m])' \
  --start=2024-06-01T00:00:00Z --end=2024-06-01T01:00:00Z --step=60s http://localhost:9090

# Top 5 busiest paths last hour
curl -s 'http://localhost:9090/api/v1/query?query=topk(5,%20sum%20by%20(path)(rate(http_requests_total[1h])))' | jq '.data.result[].metric.path'

# Deployment churn detection
curl -s 'http://localhost:9090/api/v1/query?query=changes(http_up[1h])' | jq '.data.result'

# Create a daily log index
curl -s -X PUT localhost:9200/api-logs-2024.06.01 | jq '.acknowledged'

# Count 500s in logs
curl -s 'http://localhost:9200/api-logs-*/_search?q=status:500&size=10' | jq '.hits.total.value'
```

## Alert rule example (rules.yml)
```yaml
groups:
  - name: api
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) > 0.05
        for: 10m
```

## Best practices
- Validate rules with promtool before deploying
- Use changes()/predict_linear for anomaly correlation
- Keep log indices date-based for retention

## Testing
```bash
promtool check rules rules.yml
curl -s 'http://localhost:9090/api/v1/alerts' | jq '.data.alerts[] | {name: .labels.alertname, state}'
```

## Capabilities

### analytics-deep
Advanced analytics queries and log correlation

**Parameters:**
- `index` (string): Elasticsearch index pattern, e.g. api-logs-*
- `query` (string): PromQL or ES query string
- `range` (string): Time range for analysis

**Commands:**
- `curl -G 'http://localhost:9090/api/v1/query_range' --data-urlencode 'query=rate(http_requests_total[5m])' --data-urlencode 'start=2024-06-01T00:00:00Z' --data-urlencode 'end=2024-06-01T01:00:00Z' --data-urlencode 'step=60' | jq '.data.result[0].values | length'`
- `curl -s -X PUT localhost:9200/api-logs-2024.06.01 | jq '.acknowledged'`
- `curl -s 'http://localhost:9200/api-logs-*/_search?q=status:500&size=10' | jq '.hits.total.value'`
- `promtool query range 'rate(http_requests_total[1m])' --start=2024-06-01T00:00:00Z --end=2024-06-01T01:00:00Z --step=60s http://localhost:9090`
- `curl -s 'http://localhost:9090/api/v1/query?query=topk(5,%20sum%20by%20(path)(rate(http_requests_total[1h])))' | jq '.data.result[].metric.path'`

**Examples:**
- curl -s 'http://localhost:9090/api/v1/query?query=changes(http_up[1h])' | jq '.data.result'
- curl -s 'http://localhost:9200/api-logs-*/_search?q=method:POST%20AND%20status:[400%20TO%20499]&size=5' | jq '.hits.hits[]._source'
- promtool query instant 'avg_over_time(http_request_duration_seconds_sum[1d])/avg_over_time(http_request_duration_seconds_count[1d])' http://localhost:9090

## References
- [PromQL Documentation](https://prometheus.io/docs/prometheus/latest/querying/functions/)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)