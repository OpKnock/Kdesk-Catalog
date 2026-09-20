# Newrelic Logs

Ingests logs into New Relic via the Logs API, configures Fluent Bit and Fluentd forwarders, and queries logs with NRQL for alerting and debugging.

## Instructions

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

**Commands:**
- `curl -X POST https://log-api.newrelic.com/log/v1 -H "Api-Key: $NR_LICENSE_KEY" -d @log.json`
- `curl -X POST 'https://log-api.newrelic.com/log/v1?Api-Key=$NR_LICENSE_KEY' -H 'Content-Type: application/json' -d '{"logs":[{"message":"hello"}]}'`
- `curl -s -X POST 'https://api.newrelic.com/v2/alerts_nrql_conditions.json' -H 'Api-Key: $NR_API_KEY' -d @alert.json`
- `newrelic nerdgraph query --apiKey $NR_API_KEY --query '{ actor { nrql( query: "SELECT count(*) FROM Log SINCE 1 hour ago" ) } }'`

**Examples:**
- curl -X POST https://log-api.newrelic.com/log/v1 -H "Api-Key: $NR_LICENSE_KEY" -d '{"logs":[{"timestamp":1710000000000,"message":"order placed","attributes":{"service":"orders"}}]}'
- newrelic nerdgraph query --apiKey $NR_API_KEY --query '{ actor { nrql( query: "SELECT * FROM Log WHERE service = 'orders' SINCE 1 day ago" ) } }'