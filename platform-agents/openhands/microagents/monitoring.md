---
name: "monitoring"
description: "End-to-end monitoring stack operations: Prometheus targets, Grafana datasources and dashboards, alerting rules, and uptime checks."
type: knowledge
triggers: ["monitoring", "monitoring-stack"]
---

# Monitoring

End-to-end monitoring stack operations: Prometheus targets, Grafana datasources and dashboards, alerting rules, and uptime checks.

## Instructions

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
