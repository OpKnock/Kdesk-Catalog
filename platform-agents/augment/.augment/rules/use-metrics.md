---
type: agent_requested
description: "Operates Prometheus metrics day-to-day. Reads exposition format from /metrics endpoints, executes instant and range queries via the HTTP API, reloads configuration, and verifies scrape target health. Use when working with prometheus metrics, api, observability or when the user mentions prometheus metrics, api, observability."
---

Operates Prometheus metrics day-to-day. Reads exposition format from /metrics endpoints, executes instant and range queries via the HTTP API, reloads configuration, and verifies scrape target health.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s localhost:9090/metrics | head -30`
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