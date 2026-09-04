---
name: "api-monitor-logcli"
description: "Monitors API logs with Loki and LogCLI: label-based querying, logQL pipelines, error-rate derivation, and alerting on log patterns."
type: knowledge
triggers: ["api-monitor-logcli", "logcli", "logql-pipelines"]
---

# Api Monitor Logcli

Monitors API logs with Loki and LogCLI: label-based querying, logQL pipelines, error-rate derivation, and alerting on log patterns.

## Instructions

# API Monitor v4 - Loki/LogCLI

Log-based API monitoring with Loki.

## What This Skill Does
- Queries structured API logs by labels
- Derives error rates with LogQL aggregation
- Alerts on log patterns that indicate failures

## When to Use
- Debugging API failures from log evidence
- Correlating errors across services by trace_id label
- Cost-effective alternative to full metric instrumentation

## Real Commands

```bash
logcli query '{app="api"}' --from=2h
logcli query 'rate({app="api"} |= "ERROR" [5m])'
logcli query '{app="api"} | json | status_code >= 500'
```

## LogQL Pipeline
- | json  parses structured fields
- | label_format adds derived labels
- | line_format re-renders output lines
- | unwrap latency_ms extracts numeric fields for aggregation

## Alerting
```yaml
groups:
  - name: api-errors
    rules:
      - alert: APIErrorRateHigh
        expr: sum(rate({app="api"} | json | status_code=500 [5m])) > 0.05
```

## Best Practices
- Emit structured JSON logs with stable labels
- Use |= filters before parsing for cheaper queries
- Set retention to match compliance needs

## Capabilities

### logcli
Query and tail API logs stored in Loki

**Commands:**
- `logcli query '{app="api-gateway"}' --from=2h`
- `logcli query 'rate({app="api"} |= "ERROR" [5m])'`
- `logcli query '{app="api"} | json | status_code >= 500 | line_format "{{.message}}"'`
- `logcli labels`
- `curl -s -G 'http://localhost:3100/loki/api/v1/query_range' --data-urlencode 'query={app="api"}' --data-urlencode 'limit=10' | jq '.data.result[0].values[0]'`

**Examples:**
- logcli query '{app="api"} | json | status_code=500' finds 5xx lines
- logcli labels lists available label names
- rate(... |= "ERROR" [5m]) computes error rate over the last 5 minutes

### logql-pipelines
Parse and filter structured API logs with LogQL

**Commands:**
- `logcli query '{app="api"} | json | latency_ms > 1000 | drop timestamp'`
- `curl -s -G 'http://localhost:3100/loki/api/v1/labels' | jq '.data.values'`
- `logcli series '{app=~"api.+"}'`

**Examples:**
- -cli --help
- -api --help
