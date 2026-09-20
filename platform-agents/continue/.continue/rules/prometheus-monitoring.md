---
name: "Prometheus Monitoring"
description: "Prometheus server operations: config, relabeling, recording rules, queries via promtool, and API access."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Prometheus Monitoring

Prometheus server operations: config, relabeling, recording rules, queries via promtool, and API access.

## Instructions

# Prometheus Monitoring

Run and operate the Prometheus server itself: configs, targets, rules and queries.

## What this skill does

- Starts Prometheus with validated config
- Checks rules and runs queries with promtool
- Reloads config and inspects targets

## When to use

- Setting up scraping for a new environment
- Debugging missing or duplicated targets

## Real commands

```bash
# Run
prometheus --config.file=prometheus.yml --storage.tsdb.path=/data/prom

# Validate before reload
promtool check config prometheus.yml
promtool check rules rules.yml

# Reload without restart
curl -X POST http://localhost:9090/-/reload

# Queries
promtool query instant 'sum(rate(http_requests_total[5m]))' --url http://localhost:9090
promtool query range 'http_requests_total' --start=... --end=... --step=30s --url http://localhost:9090

# Targets
curl -s 'http://localhost:9090/api/v1/targets' | jq '.data.activeTargets[].health'
```

## prometheus.yml essentials

```yaml
global:
  scrape_interval: 15s
scrape_configs:
- job_name: app
  static_configs:
  - targets: ['localhost:8080']
```

## Best practices

- Run promtool check config in CI
- Use -/reload instead of restarts
- Alert on up == 0 for every job

## Capabilities

### prometheus-operations
Run Prometheus, validate config and rules, run instant/range queries and manage targets.

**Commands:**
- `prometheus --config.file=prometheus.yml --storage.tsdb.path=/data/prom`
- `promtool check config prometheus.yml`
- `promtool check rules rules.yml`
- `promtool query instant 'http_requests_total' --url http://localhost:9090`
- `curl -X POST http://localhost:9090/-/reload`

**Examples:**
- promtool query instant 'sum(rate(http_requests_total[5m]))' --url http://localhost:9090
- promtool check config prometheus.yml && promtool check rules rules.yml
- curl -s 'http://localhost:9090/api/v1/targets' | jq '.data.activeTargets[].health' | sort | uniq -c