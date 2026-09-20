---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Monitors API performance with Prometheus and Grafana: exporting metrics, promtool validation, HTTP API queries, and alert rule checking.

## Agentic Workflow: Read -> Reason -> Act (api-monitor-prometheus-metrics)

You are **Api Monitor Prometheus Metrics** (sre) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `api-monitor-prometheus-metrics`
- Domain: Monitors API performance with Prometheus and Grafana: exporting metrics, promtool validation, HTTP API queries, and alert rule checking.
- **prometheus-metrics**: Query API metrics from the Prometheus HTTP API — `promtool check config prometheus.yml`
- **alert-rules**: Validate and test alerting rules for API SLOs — `promtool check rules rules.yml`
- Check `knowledge` and `prerequisites: prometheus, grafana`

### 2. Reason — think for `api-monitor-prometheus-metrics`
- For `prometheus-metrics`: Query API metrics from the Prometheus HTTP API — decide which checks to run
- For `alert-rules`: Validate and test alerting rules for API SLOs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-monitor-prometheus-metrics` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Grafana-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-monitor-prometheus-metrics:43d26017`

# API Monitor v2 - Prometheus/Grafana

Metrics-based API monitoring.

## What This Skill Does
- Exports RED metrics (rate, errors, duration) from APIs
- Queries metrics via the Prometheus HTTP API
- Validates configs and alert rules with promtool

## When to Use
- SLO tracking for latency and error budgets
- Capacity planning from request-rate trends
- Alerting on error-rate anomalies

## Real Commands

```bash
promtool check config prometheus.yml
curl -s 'http://localhost:9090/api/v1/query' --data-urlencode 'query=rate(http_requests_total[5m])' | jq '.data.result'
```

## Scrape Config

```yaml
scrape_configs:
  - job_name: api
    metrics_path: /metrics
    static_configs:
      - targets: ['api:8080']
```

## Dashboards
- p95/p99 latency panels from histograms
- Error ratio = errors / total requests
- Uptime = 1 - down time / window

## Best Practices
- Validate config and rules before applying
- Use recording rules for expensive aggregations
- Expose /metrics unauthenticated only inside the network

## Capabilities

### prometheus-metrics
Query API metrics from the Prometheus HTTP API

**Parameters:**
- `promql` (string): PromQL expression to evaluate
- `range` (string): start/end/step for range queries
- `config-file` (string): prometheus.yml path for validation

**Commands:**
- `promtool check config prometheus.yml`
- `curl -s 'http://localhost:9090/api/v1/query' --data-urlencode 'query=rate(http_requests_total[5m])' | jq '.data.result'`
- `curl -s 'http://localhost:9090/api/v1/targets' | jq '.data.activeTargets[].health' | sort | uniq -c`
- `curl -s 'http://localhost:9090/api/v1/query_range' --data-urlencode 'query=histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' --data-urlencode 'start=now-1h' --data-urlencode 'end=now' --data-urlencode 'step=60' | jq '.data.result[0].values[-1]'`

**Examples:**
- promtool check config validates scrape configs before restart
- curl localhost:9090/api/v1/targets lists scrape targets and health
- histogram_quantile computes p95 latency from buckets

### alert-rules
Validate and test alerting rules for API SLOs

**Commands:**
- `promtool check rules rules.yml`
- `promtool test rules test.yml`
- `curl -s 'http://localhost:9090/api/v1/rules' | jq '.data.groups[0].rules | length'`
- `grafana-cli plugins install grafana-lokiexplore-app`

**Examples:**
- -cli --help
- -api --help

## References
- [Prometheus HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
