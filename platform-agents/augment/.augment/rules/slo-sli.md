---
type: agent_requested
description: "Defines Service Level Indicators and computes SLO error budgets from Prometheus metrics. Evaluates availability and latency SLIs over 30-day windows, validates recording rules with promtool, and enables burn-rate alerting. Use when working with slo computation, api or when the user mentions slo computation, api."
---

Defines Service Level Indicators and computes SLO error budgets from Prometheus metrics. Evaluates availability and latency SLIs over 30-day windows, validates recording rules with promtool, and enables burn-rate alerting.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `promtool query instant --url=http://localhost:9090 'rate(htt`
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

# SLO / SLI

Hand-crafted skill for defining SLIs and computing SLO error budgets.

## What this skill does

- Computes availability and latency SLIs from Prometheus counters
- Evaluates error budget burn over 30d windows
- Validates recording rules with promtool before deploying

## When to use

- Defining reliability targets for a new service
- Checking whether an incident burned the budget
- Alerting on burn rate instead of raw errors

## Real commands

```bash
# Error rate over 5m
promtool query instant --url=http://localhost:9090 'rate(http_requests_total{job="api",code=~"5.."}[5m])'

# Total requests per hour
curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total[1h]))' | jq '.data.result'

# 30-day availability SLI: good / total
curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total{job="api",code!~"5.."}[30d])) / sum(rate(http_requests_total{job="api"}[30d]))' | jq '.data.result[0].value[1]'

# p99 latency from a histogram
curl -g 'http://localhost:9090/api/v1/query?query=histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq '.data.result[0].value[1]'

# Validate SLO rules before reload
promtool check rules slo.rules.yml
```

## Error budget rule

```yaml
groups:
  - name: slo.rules
    rules:
      - record: slo:api:error_budget_remaining
        expr: 1 - ((1 - sli:api:availability:ratio30d) / 0.01)
```

## Testing

```bash
promtool check rules slo.rules.yml
promtool query instant --url=http://localhost:9090 'slo:api:error_budget_remaining'
```

## Best practices

- Pick SLIs you can measure: availability from status codes, latency from histograms
- Use 30d windows for budget; alert on fast burn (5% budget in 6h)
- Never change the SLI definition retroactively

## Capabilities

### slo-computation
Defines Service Level Indicators and computes SLO error budgets from Prometheus metrics. Evaluates availability and latency SLIs over 30-day windows, validates recording rules with promtool, and enables burn-rate alerting.

**Parameters:**
- `prometheus_url` (string): Prometheus server URL (e.g., http://localhost:9090)
- `job_name` (string): Prometheus job label to query
- `window` (string): Time window for SLI calculation (e.g., 30d, 5m)

**Commands:**
- `promtool query instant --url=http://localhost:9090 'rate(http_requests_total{job="api",code=~"5.."}[5m])'`
- `curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total[1h]))' | jq '.data.result'`
- `curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total{job="api",code!~"5.."}[30d])) / sum(rate(http_requests_total{job="api"}[30d]))' | jq '.data.result[0].value[1]'`
- `curl -g 'http://localhost:9090/api/v1/query?query=histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' | jq '.data.result[0].value[1]'`
- `promtool check rules slo.rules.yml`

**Examples:**
- promtool query instant --url=http://localhost:9090 'rate(http_requests_total{job="api",code=~"5.."}[5m])'
- curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total[1h]))' | jq '.data.result'
- curl -g 'http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total{job="api",code!~"5.."}[30d])) / sum(rate(http_requests_total{job="api"}[30d]))' | jq '.data.result[0].value[1]'
- promtool check rules slo.rules.yml

## References
- [Prometheus HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/)