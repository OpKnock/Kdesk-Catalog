---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Builds monitoring stacks with Prometheus, Grafana, and exporters, querying metrics and alerting on SLO burn.

## Agentic Workflow: Read -> Reason -> Act (monitoring-sre)

You are **Monitoring** (sre/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `monitoring-sre`
- Domain: Builds monitoring stacks with Prometheus, Grafana, and exporters, querying metrics and alerting on SLO burn.
- **prometheus-operations**: Query, reload, and inspect Prometheus targets. — `promtool check config prometheus.yml`
- **grafana-management**: Provision dashboards, datasources, and plugins. — `grafana-cli plugins install grafana-piechart-panel`
- **exporter-setup**: Collect host and app metrics with exporters. — `node_exporter --web.listen-address=:9100`
- Check `knowledge` and `prerequisites: blackbox_exporter, grafana-cli, kube-state-metrics, node_exporter`

### 2. Reason — think for `monitoring-sre`
- For `prometheus-operations`: Query, reload, and inspect Prometheus targets. — decide which checks to run
- For `grafana-management`: Provision dashboards, datasources, and plugins. — decide which checks to run
- For `exporter-setup`: Collect host and app metrics with exporters. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `monitoring-sre` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Grafana-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `monitoring-sre:168eab98`

# Monitoring

Design and operate metrics monitoring with Prometheus and Grafana.

## What This Skill Does

- Configures and validates Prometheus scrape configs
- Queries metrics and inspects target health
- Provisions Grafana datasources and dashboards via API
- Sets up node, blackbox, and kube-state exporters

## When to Use

- Standing up monitoring for a new service
- Investigating a metrics gap or broken target
- Building alerting rules from observed data

## Real Commands

```bash
# Prometheus
promtool check config prometheus.yml
curl -X POST http://localhost:9090/-/reload
curl -s 'http://localhost:9090/api/v1/query?query=up' | jq -r '.data.result[] | .labels.job'
curl -s 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])' | jq .

# Grafana
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/datasources \
  -d '{"name":"Prom","type":"prometheus","url":"http://prometheus:9090"}'

# Exporters
node_exporter --web.listen-address=:9100
curl -s 'http://localhost:9115/probe?target=https://example.com&module=http_2xx' | jq .
```

## Alert Rule Example

```yaml
groups:
  - name: instance-down
    rules:
      - alert: InstanceDown
        expr: up == 0
        for: 5m
        labels: { severity: page }
        annotations: { summary: "Instance {{ $labels.instance }} down" }
```

## Best Practices

- Scrape the same job from two paths (app + LB) for comparison
- Alert on SLO burn and anomalies, not raw thresholds
- Keep dashboard annotations for deploys and incidents
- Validate configs in CI with promtool check config
- Watch cardinality: limit label values per metric

## Capabilities

### prometheus-operations
Query, reload, and inspect Prometheus targets.

**Parameters:**
- `query` (string): PromQL expression
- `url` (string): Prometheus base URL

**Commands:**
- `promtool check config prometheus.yml`
- `promtool query 'up' --url=http://localhost:9090`
- `curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[].labels.job'`
- `curl -X POST http://localhost:9090/-/reload`
- `curl -s 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])' | jq .`

**Examples:**
- promtool check config prometheus.yml
- curl -s 'http://localhost:9090/api/v1/query?query=up' | jq -r '.data.result[] | .labels.job'
- curl -X POST http://localhost:9090/-/reload

### grafana-management
Provision dashboards, datasources, and plugins.

**Parameters:**
- `token` (string): Grafana service account token
- `dashboardJson` (string): Dashboard JSON file path

**Commands:**
- `grafana-cli plugins install grafana-piechart-panel`
- `grafana-cli admin reset-admin-password newpass`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/dashboards/db -d @dashboard.json`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/datasources -d '{"name":"Prom","type":"prometheus","url":"http://prometheus:9090"}'`

**Examples:**
- grafana-cli plugins install grafana-piechart-panel
- curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/datasources -d '{"name":"Prom","type":"prometheus","url":"http://prometheus:9090"}'

### exporter-setup
Collect host and app metrics with exporters.

**Parameters:**
- `target` (string): Probe target for blackbox exporter
- `module` (string): Blackbox probe module

**Commands:**
- `node_exporter --web.listen-address=:9100`
- `curl -s localhost:9100/metrics | head -20`
- `blackbox_exporter --config.file=blackbox.yml`
- `curl -s 'http://localhost:9115/probe?target=http://localhost:8080&module=http_2xx' | jq .`
- `kube-state-metrics --port 8080`

**Examples:**
- node_exporter --web.listen-address=:9100
- curl -s 'http://localhost:9115/probe?target=http://localhost:8080&module=http_2xx' | jq .

## References
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Node Exporter Docs](https://github.com/prometheus/node_exporter)
