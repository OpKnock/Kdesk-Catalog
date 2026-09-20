# Use Metrics

Operates Prometheus metrics day-to-day. Reads exposition format from /metrics endpoints, executes instant and range queries via the HTTP API, reloads configuration, and verifies scrape target health.

## Instructions

# Use Metrics

Hand-crafted skill for using Prometheus metrics day to day.

## What this skill does

- Reads the exposition format off a metrics endpoint
- Queries live and historical data via the HTTP API
- Reloads Prometheus config and checks targets

## When to use

- "Is the service up?" from the CLI
- Computing error rates and latencies on demand
- Checking scrape health of exporters

## Real commands

```bash
# Exposition format
curl -s localhost:9090/metrics | head -30

# Instant query
curl -s "localhost:9090/api/v1/query?query=up" | jq
curl -s "localhost:9090/api/v1/query?query=rate(http_requests_total[5m])" | jq

# Range query for charts
curl -s "localhost:9090/api/v1/query_range?query=rate(http_requests_total[5m])&start=1700000000&end=1700003600&step=60" | jq

# Ops
curl -X POST localhost:9090/-/reload
curl -s "localhost:9090/api/v1/targets" | jq ".data.activeTargets | length"
```

## Metric types

- counter: http_requests_total, only increases
- gauge: current queue depth, can go either way
- histogram: _bucket/_sum/_count for latency distributions

## Useful PromQL

- up == 0 (down targets)
- 100 * (1 - sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])))
- histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

## Testing

```bash
curl -s "localhost:9090/api/v1/query?query=up" | jq ".data.result | length"
curl -X POST localhost:9090/-/reload
```

## Best practices

- Always apply rate() to counters; never raw
- Use sum by (label) for multi-instance aggregates
- Check targets before debugging queries

## Capabilities

### prometheus-metrics
Expose, scrape, and query metrics

**Commands:**
- `curl -s localhost:9090/metrics | head -30`
- `curl -s "localhost:9090/api/v1/query?query=up" | jq`
- `curl -s "localhost:9090/api/v1/query?query=rate(http_requests_total[5m])" | jq`
- `curl -s "localhost:9090/api/v1/query_range?query=rate(http_requests_total[5m])&start=1700000000&end=1700003600&step=60" | jq`
- `curl -X POST localhost:9090/-/reload`
- `curl -s "localhost:9090/api/v1/targets" | jq ".data.activeTargets | length"`

**Examples:**
- curl -s "localhost:9090/api/v1/query?query=rate(http_requests_total[5m])" | jq
- curl -s localhost:9090/metrics | head -30
- curl -X POST localhost:9090/-/reload