---
name: "metrics"
description: "Instrument services with metrics: design metric names/labels, expose /metrics endpoints, and verify scrapes with promtool. Use when working with metrics instrumentation, api or when the user mentions metrics instrumentation, api."
type: knowledge
triggers: ["metrics", "metrics-instrumentation"]
---

Instrument services with metrics: design metric names/labels, expose /metrics endpoints, and verify scrapes with promtool.

## Agentic Workflow: Read -> Reason -> Act (metrics)

You are **Metrics** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `metrics`
- Domain: Instrument services with metrics: design metric names/labels, expose /metrics endpoints, and verify scrapes with promtool.
- **metrics-instrumentation**: Instrument applications with Prometheus metric types, expose an endpoint, and validate the output. — `promtool check metrics --extended /dev/stdin`
- Check `knowledge` and `prerequisites: node_exporter, promtool`

### 2. Reason — think for `metrics`
- For `metrics-instrumentation`: Instrument applications with Prometheus metric types, expose an endpoint, and validate the output. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `metrics` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Node_exporter` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `metrics:2527a1a3`

# Metrics

Instrumenting services with Prometheus-style metrics gives you counters, gauges, histograms and summaries.

## What this skill does

- Designs metric names and label sets for new services
- Exposes a `/metrics` endpoint and validates its output with promtool
- Verifies the Prometheus server is scraping successfully (`up`)

## When to use

- Adding observability to a new microservice
- Validating that scrapes and metrics are well-formed before wiring dashboards
- Fixing duplicate metric names or bad label usage

## Real commands

```bash
# Validate metric text format before shipping it
promtool check metrics --extended /dev/stdin

# Verify scrape target is up
curl -s http://localhost:9090/api/v1/query?query=up

# Inspect a node_exporter textfile metric
curl -s http://localhost:9100/metrics | grep node_cpu_seconds_total

# Expose textfile metrics for cron jobs
node_exporter --collector.textfile.directory=/var/lib/node_exporter/textfile

# Validate scrape config
promtool check config /etc/prometheus/prometheus.yml
```

## Naming conventions

- Counters end in `_total`; rates use `rate(metric[5m])`
- Units in name: `_seconds`, `_bytes`, `_requests`
- Keep labels consistent across all metrics of a service

## Textfile collector example

```bash
printf 'my_batch_job_duration_seconds 42.5\n' > /var/lib/node_exporter/textfile/job.prom
```

## Best practices

- Prefix metric names with the app namespace
- Expose on a dedicated port when possible
- Never add high-cardinality labels (see metrics-cardinality-skill)

## Capabilities

### metrics-instrumentation
Instrument applications with Prometheus metric types, expose an endpoint, and validate the output.

**Parameters:**
- `port` (integer): Port the metrics endpoint listens on
- `namespace` (string): Metric namespace prefix, e.g. app_name
- `labels` (array): Consistent label set applied to every metric

**Commands:**
- `promtool check metrics --extended /dev/stdin`
- `curl -s http://localhost:9100/metrics`
- `curl -s 'http://localhost:9090/api/v1/query?query=up'`
- `node_exporter --collector.textfile.directory=/var/lib/node_exporter/textfile`
- `promtool check config /etc/prometheus/prometheus.yml`

**Examples:**
- curl -s http://localhost:9100/metrics | grep node_cpu_seconds_total
- curl -s http://localhost:9090/api/v1/query?query=up
- promtool check metrics < my_metrics.txt

## References
- [Prometheus Metric Types](https://prometheus.io/docs/concepts/metric_types/)
- [Node Exporter](https://github.com/prometheus/node_exporter)
