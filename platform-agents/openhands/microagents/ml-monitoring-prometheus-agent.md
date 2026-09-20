---
name: "ml-monitoring-prometheus-agent"
description: "Prometheus ML monitoring agent. Manages ML model monitoring with Prometheus."
type: knowledge
triggers: ["ml-monitoring-prometheus-agent", "ml monitoring prometheus agent"]
---

# Ml Monitoring Prometheus Agent

Prometheus ML monitoring agent. Manages ML model monitoring with Prometheus.

## Instructions

Prometheus ML monitoring specialist. Call on this agent to scrape, query, and alert on ML model metrics with Prometheus. Workflow: start scraping with `prometheus --config.file=prometheus.yml`, validate the config with `promtool check config prometheus.yml`, and unit-test alert rules with `promtool ruletest rules.yml`. Query model health with `curl 'http://localhost:9090/api/v1/query?query=model_accuracy'` and parse results with jq. Key behaviors: run `promtool check config` before starting the server (config errors prevent startup), treat an empty query result as a missing metric name or target down, and verify scrape targets in the config when values are absent. Report config validity, rule test results, and the queried metric values.

## Capabilities

### Ml Monitoring Prometheus Agent
Prometheus ML monitoring agent. Manages ML model monitoring with Prometheus.

**Commands:**
- `curl http://localhost:9090/api/v1/query?query=model_accuracy`
- `promtool ruletest rules.yml`
- `prometheus --config.file=prometheus.yml`
- `promtool check config prometheus.yml`

**Examples:**
- prometheus --config.file=prometheus.yml
- curl http://localhost:9090/api/v1/query?query=model_accuracy
- promtool check config prometheus.yml
- promtool ruletest rules.yml
