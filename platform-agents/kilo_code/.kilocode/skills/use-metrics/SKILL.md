---
name: "use-metrics"
description: "Operates Prometheus metrics day-to-day. Reads exposition format from /metrics endpoints, executes instant and range queries via the HTTP API, reloads configuration, and verifies scrape target health. Use when working with prometheus metrics, api, observability or when the user mentions prometheus metrics, api, observability."
license: "MIT"
compatibility: "Requires curl, jq. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*)"
---

Operates Prometheus metrics day-to-day. Reads exposition format from /metrics endpoints, executes instant and range queries via the HTTP API, reloads configuration, and verifies scrape target health.

## Agentic Workflow: Read -> Reason -> Act (use-metrics)

You are **Use Metrics** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `use-metrics`
- Domain: Operates Prometheus metrics day-to-day. Reads exposition format from /metrics endpoints, executes instant and range queries via the HTTP API, reloads configuration, and verifies scrape target health.
- **prometheus-metrics**: Expose, scrape, and query metrics — `curl -s localhost:9090/metrics | head -30`
- Check `knowledge` and `prerequisites: curl, jq`

### 2. Reason — think for `use-metrics`
- For `prometheus-metrics`: Expose, scrape, and query metrics — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `use-metrics` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `use-metrics:a097ce5b`

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

**Parameters:**
- `query` (string): PromQL expression
- `start` (integer): Start unix time for range queries
- `end` (integer): End unix time for range queries

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

## References
- [Prometheus HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/)
- [PromQL basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus best practices](https://prometheus.io/docs/practices/naming/)
