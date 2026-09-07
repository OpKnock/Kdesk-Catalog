Diagnose and fix high-cardinality metric problems in Prometheus: find exploding label values, top series, and identify offending scrape targets.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `promtool tsdb analyze --help`
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

# Metrics Cardinality

High cardinality (too many unique label-value combinations) is the #1 cause of Prometheus memory and disk exhaustion.

## What this skill does

- Analyzes the TSDB to find which metric names generate the most series
- Lists the label value counts driving cardinality (e.g. per-endpoint, per-user)
- Recommends fixes: relabeling, metric redesign, or aggregation

## When to use

- Prometheus memory spikes or OOM kills on `metric_relabel_configs` host
- Dashboards are slow and `count by` queries time out
- An endpoint suddenly creates millions of series

## Real commands

```bash
# Analyze whole TSDB for cardinality report
promtool tsdb analyze /var/lib/prometheus/metrics2/

# List all series for a metric
promtool tsdb series --match 'http_requests_total{status=~".+"}' /var/lib/prometheus/metrics2/

# Top 20 metric names by series count (HTTP API)
curl -g 'http://localhost:9090/api/v1/query?query=topk(20,count%20by%20(__name__)({__name__=~".+"}))'

# Which endpoints/methods dominate a metric
curl -g 'http://localhost:9090/api/v1/query?query=count%20by%20(endpoint,%20method)(http_requests_total)'
```

## Fixing it

```yaml
# Drop the offending label at scrape time
metric_relabel_configs:
- source_labels: [user_id]
  regex: '.*'
  action: drop

# Or aggregate away the cardinality in recording rules
- record: job:http_requests_total:rate5m
  expr: sum(rate(http_requests_total[5m])) by (job)
```

## Best practices

- Limit label values that are unbounded (user IDs, emails, IPs)
- Keep cardinality per metric under ~10k series
- Set `--storage.tsdb.retention.time` and alert on `prometheus_tsdb_head_series`

## Capabilities

### cardinality-diagnosis
Analyze a Prometheus TSDB to find high-cardinality series, top label combinations, and memory-heavy metrics.

**Parameters:**
- `db_path` (string): Path to the Prometheus TSDB directory
- `match` (string): Label matcher used to filter series
- `topk` (integer): Number of highest-cardinality metrics to return

**Commands:**
- `promtool tsdb analyze --help`
- `promtool tsdb analyze /var/lib/prometheus/metrics2/`
- `promtool tsdb series --match '{__name__=~".+"}' /var/lib/prometheus/metrics2/`
- `curl -g 'http://localhost:9090/api/v1/query?query=topk(20,count%20by%20(__name__)({__name__%3D~%22.%2B%22}))'`
- `curl -g 'http://localhost:9090/api/v1/query?query=count%20by%20(endpoint%2C%20method)(http_requests_total)'`

**Examples:**
- promtool tsdb analyze /var/lib/prometheus/metrics2/
- curl -g 'http://localhost:9090/api/v1/query?query=topk(10,count%20by%20(__name__)({__name__=~".+"}))'
- promtool tsdb series --match 'http_requests_total{status=~".*"}' /var/lib/prometheus/metrics2/

## References
- [Prometheus Cardinality Best Practices](https://prometheus.io/docs/practices/instrumentation/)
- [promtool TSDB docs](https://prometheus.io/docs/prometheus/latest/command-line/promtool/)