---
trigger: glob
description: "Ingests logs into New Relic via the Logs API, configures Fluent Bit and Fluentd forwarders, and queries logs with NRQL for alerting and debugging. Use when working with newrelic logs ingestion, api or when the user mentions newrelic logs ingestion, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

Ingests logs into New Relic via the Logs API, configures Fluent Bit and Fluentd forwarders, and queries logs with NRQL for alerting and debugging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST https://log-api.newrelic.com/log/v1 -H "Api-Key`
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

# New Relic Logs

Ship application logs to New Relic for centralized search, alerting and correlation with metrics/traces.

## What this skill does

- Ingests logs via the HTTP Logs API
- Configures Fluent Bit/FluentD forwarding
- Queries logs with NRQL

## When to use

- Centralizing logs across services
- Alerting on log patterns

## Real commands

```bash
# Ingest a single log line
curl -X POST https://log-api.newrelic.com/log/v1 \
  -H "Api-Key: $NR_LICENSE_KEY" \
  -d '{"logs":[{"timestamp":1710000000000,"message":"order placed","attributes":{"service":"orders"}}]}'

# Query via GraphQL/NRQL
newrelic nerdgraph query --apiKey $NR_API_KEY \
  --query '{ actor { nrql( query: "SELECT count(*) FROM Log WHERE service = 'orders' SINCE 1 day ago" ) } }'
```

## Fluent Bit output

```ini
[OUTPUT]
    Name  http
    Match *
    Host  log-api.newrelic.com
    Port  443
    URI   /log/v1
    Header Api-Key ${NR_LICENSE_KEY}
```

## Best practices

- Add structured attributes (service, level, trace.id)
- Batch logs to avoid rate limits
- Set NRQL alert conditions on error patterns

## Capabilities

### newrelic-logs-ingestion
Send logs to New Relic via the Logs API and query them with NRQL.

**Parameters:**
- `api_key` (string): New Relic license or API key
- `message` (string): Log message content
- `attributes` (object): Key-value attributes attached to the log

**Commands:**
- `curl -X POST https://log-api.newrelic.com/log/v1 -H "Api-Key: $NR_LICENSE_KEY" -d @log.json`
- `curl -X POST 'https://log-api.newrelic.com/log/v1?Api-Key=$NR_LICENSE_KEY' -H 'Content-Type: application/json' -d '{"logs":[{"message":"hello"}]}'`
- `curl -s -X POST 'https://api.newrelic.com/v2/alerts_nrql_conditions.json' -H 'Api-Key: $NR_API_KEY' -d @alert.json`
- `newrelic nerdgraph query --apiKey $NR_API_KEY --query '{ actor { nrql( query: "SELECT count(*) FROM Log SINCE 1 hour ago" ) } }'`

**Examples:**
- curl -X POST https://log-api.newrelic.com/log/v1 -H "Api-Key: $NR_LICENSE_KEY" -d '{"logs":[{"timestamp":1710000000000,"message":"order placed","attributes":{"service":"orders"}}]}'
- newrelic nerdgraph query --apiKey $NR_API_KEY --query '{ actor { nrql( query: "SELECT * FROM Log WHERE service = 'orders' SINCE 1 day ago" ) } }'

## References
- [New Relic Logs Docs](https://docs.newrelic.com/docs/logs/)
- [Logs API reference](https://docs.newrelic.com/docs/logs/logs-api/introduction-logs-api/)
