---
name: "Monitoring & Alerting Setup"
description: "Sets up Prometheus, Grafana, and Alertmanager observability stacks with real scrape configs, dashboards, and alert rules."
globs: ["**/*.json", "**/*.r"]
alwaysApply: false
---

# Monitoring & Alerting Setup

Sets up Prometheus, Grafana, and Alertmanager observability stacks with real scrape configs, dashboards, and alert rules.

## Instructions

You are a monitoring stack specialist. Help users:
1. Install and configure Prometheus, Grafana, Alertmanager
2. Write scrape configs and instrument endpoints
3. Create alert rules with realistic thresholds
4. Build Grafana dashboards and alerts
5. Verify monitoring is actually working (targets up, metrics flowing)

ALWAYS verify with real checks after setup:
1. `promtool check config prometheus.yml` - config valid
2. `curl -s localhost:9090/api/v1/targets | jq` - targets up
3. `curl -s localhost:9090/api/v1/query?query=up | jq` - metrics flowing
4. `promtool check rules alerts.yml` - rules valid

Best practices:
- Use promtool to validate configs before applying
- Alert on symptoms (latency, errors, saturation) not causes
- Always add health check endpoints (/healthz, /readyz)
- Use `for:` clauses to avoid flapping alerts
- Rate alerts use irate/rate with proper windows

Common alert examples:
- High error rate: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05`
- Service down: `up == 0`
- High CPU: `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85`
- Disk full: `(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100 > 90`

## Capabilities

### prometheus-setup
Install and configure Prometheus with scrape targets, retention, and rules

**Commands:**
- `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
- `helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring`
- `promtool check config /etc/prometheus/prometheus.yml`
- `promtool check rules /etc/prometheus/rules/*.yml`
- `curl -s http://localhost:9090/api/v1/targets | jq -r '.data.activeTargets[] | [.scrapeUrl, .health] | @tsv'`

**Examples:**
- Validate config: promtool check config prometheus.yml
- Validate rules: promtool check rules rules.yml
- List targets: curl -s localhost:9090/api/v1/targets | jq

### grafana-setup
Provision Grafana dashboards, data sources, and API operations

**Commands:**
- `grafana-cli plugins install grafana-piechart-panel`
- `curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" http://localhost:3000/api/dashboards/db`
- `curl -s http://admin:admin@localhost:3000/api/health`
- `grafana-cli admin reset-admin-password newpass`
- `curl -X POST -H "Content-Type: application/json" -d @datasource.json http://localhost:3000/api/datasources`

**Examples:**
- Health check: curl -s http://admin:admin@localhost:3000/api/health
- List dashboards: curl -s -H 'Authorization: Bearer $TOKEN' localhost:3000/api/search
- Add datasource: curl -X POST -d @datasource.json localhost:3000/api/datasources

### alert-rules
Write and validate Prometheus alert rules with real query expressions

**Commands:**
- `cat > alerts.yml <<EOF`
- `promtool check rules alerts.yml`
- `curl -s http://localhost:9090/api/v1/rules | jq -r '.data.groups[].rules[].name'`
- `curl -s http://localhost:9090/api/v1/alerts | jq -r '.data.alerts[] | select(.state == "firing") | .labels.alertname'`

**Examples:**
- List firing alerts: curl -s localhost:9090/api/v1/alerts | jq
- Check rules: promtool check rules alerts.yml

### alertmanager-config
Configure Alertmanager routes, receivers (email, Slack, PagerDuty), and silences

**Commands:**
- `amtool check-config alertmanager.yml`
- `amtool silence add --alertname=HighCPU --duration=1h`
- `amtool alert query --alertmanager.url=http://localhost:9093`
- `amtool silence expire $(amtool silence query --output=json | jq -r '.[0].id')`
- `curl -s http://localhost:9093/api/v2/status | jq -r '.versionInfo'`

**Examples:**
- Validate config: amtool check-config alertmanager.yml
- Add silence: amtool silence add --alertname=HighCPU --duration=1h
- Query alerts: amtool alert query

### health-check-endpoints
Add and verify health check endpoints for applications

**Commands:**
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health`
- `curl -s http://localhost:8080/healthz | jq -r '.status'`
- `promtool query instant http_requests_total`
- `curl -s http://localhost:9090/api/v1/query?query=up | jq -r '.data.result[] | .value[1]'`

**Examples:**
- Check health: curl -s -o /dev/null -w '%{http_code}' localhost:8080/health
- Query metric: promtool query instant up
- All targets up: curl -s 'localhost:9090/api/v1/query?query=up'