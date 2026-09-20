Queries Prometheus for live monitoring: PromQL, the HTTP API, targets health, and ad-hoc alert inspection.

## Agentic Workflow: Read -> Reason -> Act (prometheus-monitoring-2)

You are **prometheus-monitoring-2** (monitoring/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — monitoring context for `prometheus-monitoring-2`
- Domain: Queries Prometheus for live monitoring: PromQL, the HTTP API, targets health, and ad-hoc alert inspection.
- **api-query**: Query Prometheus data with the HTTP API. — `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up'`
- **promql**: Write and validate PromQL for dashboards and alerts. — `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=sum by (job) `
- Check `knowledge` references before acting

### 2. Reason — think for `prometheus-monitoring-2`
- For `api-query`: Query Prometheus data with the HTTP API. — decide which checks to run
- For `promql`: Write and validate PromQL for dashboards and alerts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `prometheus-monitoring-2` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `prometheus-monitoring-2:94ce1ef4`

# Prometheus Monitoring

Answer live monitoring questions directly from the API.

## When to Use

- On-call queries during incidents
- Validating dashboards and alerts
- Auditing target health

## Target health

```bash
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {scrapeUrl, health}'
```

## Instant queries

```bash
curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up{job="api"}'
curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=rate(http_requests_total[5m])'
```

## Range queries

```bash
curl -G http://localhost:9090/api/v1/query_range --data-urlencode 'query=node_memory_Active_bytes' --data-urlencode 'start=...' --data-urlencode 'end=...' --data-urlencode 'step=60'
```

## Common recipes

- CPU: `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
- Error rate: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
- Restarts: `changes(process_start_time_seconds[15m]) > 0`
- p99: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`

## Alerts

```bash
curl -s http://localhost:9090/api/v1/alerts | jq '.data.alerts[] | {name: .labels.alertname, state}'
```

## Best practices

- Prefer rates over raw counters in dashboards.
- Use recording rules for expensive queries.
- Check label cardinality quarterly via /api/v1/series.
- Timeout every ad-hoc query to avoid long API hangs.

## Testing

```bash
curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up' | jq '.data.result | length'
```

Assert expected target counts after config changes.

## Capabilities

### api-query
Query Prometheus data with the HTTP API.

**Parameters:**
- `query` (string): PromQL expression
- `step` (number): Query range step in seconds
- `timeout` (string): Query timeout

**Commands:**
- `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up'`
- `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=rate(http_requests_total[5m])'`
- `curl -G http://localhost:9090/api/v1/query_range --data-urlencode 'query=node_cpu_seconds_total' --data-urlencode 'start=1750000000' --data-urlencode 'end=1750086400' --data-urlencode 'step=60'`
- `curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {scrapeUrl, health}'`
- `curl -s http://localhost:9090/api/v1/alerts | jq '.data.alerts[] | {name: .labels.alertname, state}'`

**Examples:**
- curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
- curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))' | jq '.data.result'
- curl -s http://localhost:9090/api/v1/targets | jq '[.data.activeTargets[] | select(.health=="down")] | length'

### promql
Write and validate PromQL for dashboards and alerts.

**Parameters:**
- `match` (string): Series matcher for /series
- `labels` (string): Label name to list values
- `topk` (number): Top-N aggregation

**Commands:**
- `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=sum by (job) (rate(http_requests_total[5m]))'`
- `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=sum(rate(container_cpu_usage_seconds_total[5m])) by (namespace)'`
- `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=changes(process_start_time_seconds{job="api"}[15m]) > 0'`
- `curl -s http://localhost:9090/api/v1/labels | jq '.data'`
- `curl -G http://localhost:9090/api/v1/series --data-urlencode 'match[]=up' | jq '.data | length'`

**Examples:**
- curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=rate(node_network_receive_bytes_total[5m])'
- curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))' | jq '.data.result[0].value[1]'
- curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=topk(5, sum by (job) (rate(http_requests_total[5m])))'

## References
- [Prometheus Querying](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/)
- [Querying examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
