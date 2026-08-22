# api-analytics-engineer

Implement API analytics with usage tracking, performance metrics, and developer dashboards: instrument endpoints, store metrics, and build dashboards.

## Instructions

# API Analytics Engineer

## What this skill does
Implement API analytics: instrument endpoints with Prometheus counters/histograms, track usage and error rates, expose a metrics endpoint, and build Grafana dashboards for developers.

## When to use
- Adding usage/performance tracking to an API
- Building developer dashboards
- Alerting on error rates and latency

## Real commands
```bash
# Validate config and reload Prometheus
promtool check config prometheus.yml
curl -X POST http://localhost:9090/-/reload

# Requests per second over 5m
curl -s 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])' | jq '.data.result[0].value'

# p99 latency
curl -s 'http://localhost:9090/api/v1/query?query=histogram_quantile(0.99,%20sum(rate(http_request_duration_seconds_bucket[5m]))%20by%20(le))' | jq '.data.result'

# 5xx rate
curl -s 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total{status=~"5.."}[5m]))' | jq '.data.result[0].value[1]'

# Start Grafana
docker run -d -p 3000:3000 grafana/grafana

# App metrics endpoint
curl -s http://localhost:8080/api/metrics | jq '.counters'
```

## Instrumentation example (Prometheus client)
```js
const counter = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total API requests',
  labelNames: ['method', 'path', 'status']
});
counter.inc({ method: req.method, path: req.path, status: res.statusCode });
```

## Dashboard panels
- RPS per endpoint
- p50/p95/p99 latency
- Error rate by status class
- Top consumers by API key

## Best practices
- Label cardinality discipline: use templated paths, never raw paths
- Use histograms with pre-bounded buckets
- Expose /metrics on a separate port in production

## Testing
```bash
promtool check config prometheus.yml
curl -s 'http://localhost:9090/api/v1/query?query=up' | jq '.data.result'
```

## Capabilities

### analytics-pipeline
Instrument APIs and build analytics dashboards

**Commands:**
- `promtool check config prometheus.yml`
- `curl -X POST http://localhost:9090/-/reload`
- `curl -s 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])' | jq '.data.result[0].value'`
- `docker run -d -p 3000:3000 grafana/grafana`
- `curl -s -X POST http://localhost:8080/api/metrics | jq '.counters'`

**Examples:**
- curl -s 'http://localhost:9090/api/v1/query?query=histogram_quantile(0.99,%20sum(rate(http_request_duration_seconds_bucket[5m]))%20by%20(le))' | jq '.data.result'
- curl -s 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total{status=~"5.."}[5m]))' | jq '.data.result[0].value[1]'
- promtool query instant 'http_requests_total' http://localhost:9090
