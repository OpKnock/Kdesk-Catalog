---
trigger: glob
description: "Instrument services with metrics: design metric names/labels, expose /metrics endpoints, and verify scrapes with promtool. Use when working with metrics instrumentation, api or when the user mentions metrics instrumentation, api."
globs: ["**/*.r", "**/*.sh"]
---

Instrument services with metrics: design metric names/labels, expose /metrics endpoints, and verify scrapes with promtool.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `promtool check metrics --extended /dev/stdin`
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
