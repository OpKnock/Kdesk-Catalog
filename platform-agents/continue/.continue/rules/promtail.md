---
name: "Promtail"
description: "Promtail log shipping to Loki: config, file discovery, labels, pipeline stages and logcli queries."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Promtail

Promtail log shipping to Loki: config, file discovery, labels, pipeline stages and logcli queries.

## Instructions

# Promtail

Promtail tails log files, adds labels, and pushes them to Loki for querying.

## What this skill does

- Configures file discovery and labels
- Transforms lines with pipeline stages
- Queries Loki with logcli

## When to use

- Shipping app logs to Loki
- Parsing structured fields from log lines

## Real commands

```bash
# Run promtail
promtail -config.file=promtail.yaml
promtail -config.file=promtail.yaml -dry-run

# Push test entry (Loki push API)
curl -X POST http://localhost:3100/loki/api/v1/push -H "Content-Type: application/json" \
  -d '{"streams":[{"stream":{"job":"app"},"values":[["1710000000000000000","log line"]]}]}'

# Query
logcli query '{job="app"}' --limit 50
logcli query '{job="app"} |= "error"' --from "1h ago"
logcli labels
```

## promtail.yaml

```yaml
server:
  http_listen_port: 9080
clients:
- url: http://localhost:3100/loki/api/v1/push
scrape_configs:
- job_name: app
  static_configs:
  - targets: [localhost]
    labels:
      job: app
      __path__: /var/log/app/*.log
```

## Best practices

- Keep labels low-cardinality (job, env, service)
- Use -dry-run to preview labels before pushing
- Use json/regex stages to extract structured fields

## Capabilities

### promtail-log-shipping
Run promtail with configs, process log lines with pipelines, and query Loki with logcli.

**Commands:**
- `promtail -config.file=promtail.yaml`
- `curl -X POST http://localhost:3100/loki/api/v1/push -H "Content-Type: application/json" -d '{"streams":[{"stream":{"job":"app"},"values":[["1710000000000000000","log line"]]}]}'`
- `logcli query '{job="app"}' --limit 50`
- `logcli query '{job="app"} |= "error"' --from "1h ago"`
- `logcli labels`

**Examples:**
- logcli query '{service="orders"} |= "exception" | json' --limit 100
- promtail -config.file=promtail.yaml -dry-run
- logcli query '{job="app"} |= "500"' --since 24h | wc -l