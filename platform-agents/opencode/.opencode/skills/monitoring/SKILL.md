---
name: "monitoring"
description: "End-to-end monitoring stack operations: Prometheus targets, Grafana datasources and dashboards, alerting rules, and uptime checks. Use when working with monitoring stack, api or when the user mentions monitoring stack, api."
---

End-to-end monitoring stack operations: Prometheus targets, Grafana datasources and dashboards, alerting rules, and uptime checks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d --name grafana -p 3000:3000 grafana/grafana`
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

# Monitoring

A monitoring stack turns raw metrics into alerting and dashboards.

## What this skill does

- Boots Grafana and connects it to Prometheus
- Validates alert rules with promtool and hot-reloads config
- Covers synthetic uptime and availability checks

## When to use

- Standing up observability for a new environment
- Fixing a broken scrape target or dashboard
- Adding alert rules that must not fire falsely

## Real commands

```bash
# Start Grafana
 docker run -d --name grafana -p 3000:3000 grafana/grafana

# Provision Prometheus datasource via API
curl -u admin:admin -X POST http://localhost:3000/api/datasources \
  -H "Content-Type: application/json" \
  -d '{"name":"Prometheus","type":"prometheus","url":"http://prometheus:9090"}'

# Validate alert rules and reload
promtool check rules /etc/prometheus/rules.yml
curl -X POST http://localhost:9090/-/reload

# Inspect active rules
curl -s http://localhost:9090/api/v1/rules
```

## Rule example

```yaml
groups:
- name: availability
  rules:
  - alert: InstanceDown
    expr: up == 0
    for: 2m
    labels: { severity: critical }
```

## Best practices

- Check rules with promtool before reloading
- Add `for:` durations to suppress transient blips
- Monitor the monitor: alert on `up == 0` for prometheus itself

## Capabilities

### monitoring-stack
Operate a Prometheus + Grafana stack: provision datasources, manage dashboards and validate alert rules.

**Parameters:**
- `url` (string): Datasource or endpoint URL
- `username` (string): Basic auth user for Grafana/API
- `rules_file` (string): Path to Prometheus alerting rules file

**Commands:**
- `docker run -d --name grafana -p 3000:3000 grafana/grafana`
- `curl -u admin:admin -X POST http://localhost:3000/api/datasources -H "Content-Type: application/json" -d '{"name":"Prometheus","type":"prometheus","url":"http://prometheus:9090"}'`
- `promtool check rules /etc/prometheus/rules.yml`
- `curl -X POST http://localhost:9090/-/reload`
- `curl -s http://localhost:9090/api/v1/alertmanagers`

**Examples:**
- curl -u admin:admin -X POST http://localhost:3000/api/datasources -d @datasource.json
- promtool check rules /etc/prometheus/rules.yml
- curl -s http://localhost:9090/api/v1/rules

## References
- [Grafana Docs](https://grafana.com/docs/grafana/latest/)
- [Prometheus Alerting](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
