---
name: "health-monitoring-engineer"
description: "Turns service health into metrics: exposes /metrics endpoints, validates with promtool, and answers ad-hoc queries against Prometheus."
---

# health-monitoring-engineer

Turns service health into metrics: exposes /metrics endpoints, validates with promtool, and answers ad-hoc queries against Prometheus.

## Instructions

# Health Monitoring

Instrument services with /metrics and validate the pipeline end-to-end.

## When to Use

- Adding Prometheus-format metrics to a service
- Verifying metric quality before dashboards rely on them
- Answering quick health questions from production data

## Expose metrics

Standard HTTP server + prometheus client:

```go
http.Handle("/metrics", promhttp.Handler())
log.Fatal(http.ListenAndServe(":9100", nil))
```

```bash
curl -s http://localhost:9100/metrics | head -40
```

## Validate with promtool

```bash
promtool check metrics http://localhost:9100/metrics --lint=error
```

Lint catches bad naming, missing units, and duplicate families before dashboards break.

## Node-level health

```bash
node_exporter --web.listen-address=:9100 --collector.filesystem
curl -s http://localhost:9100/metrics | grep '^node_load1'
```

## Answer queries

```bash
promtool query instant http://localhost:9090 'up{job="api"}'
promtool query instant http://localhost:9090 '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
```

## Best practices

- Follow Prometheus naming: `unit_verb`, e.g. `http_requests_total`.
- Add `_total` for counters and document HELP lines.
- Keep high-cardinality labels (user_id, path) out of metrics.
- Scrape from a sidecar or scraper; never rely on curl alone in prod.

## Testing

```bash
promtool check metrics http://localhost:9100/metrics --lint=error
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets | length'
```

Verify targets are up after every scrape-config change.

## Capabilities

### metrics-endpoints
Expose and validate Prometheus-format metrics.

**Commands:**
- `promtool check metrics http://localhost:9100/metrics`
- `curl -s http://localhost:9100/metrics | head -40`
- `promtool check metric-label http://localhost:9100/metrics '^up$'`
- `node_exporter --collector.textfile.directory=/var/lib/node_exporter/textfile`
- `curl -s http://localhost:9100/metrics | grep -E '^process_cpu_seconds_total'`

**Examples:**
- promtool check metrics http://localhost:9090/metrics --lint=error
- curl -s http://localhost:9100/metrics | grep '^node_memory_' | head
- node_exporter --web.listen-address=:9100 --collector.filesystem

### query
Query Prometheus for health signals.

**Commands:**
- `promtool query instant http://localhost:9090 'up'`
- `promtool query range http://localhost:9090 'rate(http_requests_total[5m])' --start=-30m`
- `curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up{job="api"}'`
- `promtool query instant http://localhost:9090 '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'`
- `curl -G http://localhost:9090/api/v1/targets | jq '.data.activeTargets | length'`

**Examples:**
- promtool query instant http://localhost:9090 'sum by (job) (up)'
- curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up' | jq '.data.result'
- promtool query range http://localhost:9090 'histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))'
