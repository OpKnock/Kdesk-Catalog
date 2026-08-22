---
trigger: glob
description: "Collects, searches, aggregates, and processes application logs with the Datadog Logs API v1/v2, covering ingestion, pipelines, and index management."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Datadog Logs

Collects, searches, aggregates, and processes application logs with the Datadog Logs API v1/v2, covering ingestion, pipelines, and index management.

## Instructions

# Datadog Logs

Collect, search, aggregate, and process application logs with the real Datadog API.

## When to Use

- Ingesting application logs into Datadog
- Searching logs for errors, latency, or specific attributes
- Aggregating logs for counts and trends
- Building parsing pipelines and managing indexes

## Setup

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-application-key"
# Datadog site defaults to US1; for EU use https://api.datadoghq.eu
export DD_SITE="datadoghq.com"
```

## Ingest Logs

```bash
# Ingest JSON logs through the intake endpoint
curl -X POST "https://http-intake.logs.datadoghq.com/api/v2/logs" \
  -H "Content-Type: application/json" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -d '{"ddsource":"api","ddtags":"env:prod,team:payments","message":"payment failed","service":"checkout","status":"error"}'
```

## Search Logs

```bash
# Search last hour of errors
curl -s -X POST "https://api.datadoghq.com/api/v2/logs/events/search" \
  -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -d '{"filter":{"query":"service:api status:error","from":"now-1h"},"page":{"limit":50}}' | jq '.data[].attributes.attributes.message'

# Aggregate error count by service
curl -s -X POST "https://api.datadoghq.com/api/v2/logs/events/aggregate" \
  -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -d '{"compute":[{"aggregation":"count"}],"group_by":[{"facet":"service"}]}'
```

## Pipelines

```bash
# List pipelines
curl -X GET "https://api.datadoghq.com/api/v1/logs/config/pipelines" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"
# Create a pipeline
curl -X POST "https://api.datadoghq.com/api/v1/logs/config/pipelines" \
  -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -d '{"name":"Parse Nginx","filter":{"query":"source:nginx"}}'
```

## Testing

```bash
# Send a test log and verify it appears in the search API within seconds
curl -s -X POST "https://api.datadoghq.com/api/v2/logs/events/search" \
  -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -d '{"filter":{"query":"service:checkout"},"page":{"limit":5}}' | jq '.meta.page.total'
```

## Best Practices

- Always set `service`, `status`, and `env` tags on ingested logs
- Use `from`/`to` with relative times such as `now-15m`
- Keep queries scoped with `service:`, `env:`, and `status:` filters
- Store secrets in env vars, never inline API keys
- Use the EU endpoint `https://api.datadoghq.eu` when the account is on the EU site

## Capabilities

### log-search
Search and aggregate logs with the Datadog Logs Search API and ingest logs with the intake API

**Commands:**
- `curl -X POST "https://api.datadoghq.com/api/v2/logs/events/search" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d @search.json`
- `curl -X POST "https://api.datadoghq.com/api/v2/logs/events/aggregate" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d @aggregate.json`
- `curl -s -X POST "https://api.datadoghq.com/api/v2/logs/events/search" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d '{"filter":{"query":"service:api status:error","from":"now-1h"}}' | jq '.data[].attributes.attributes.message'`
- `curl -X POST "https://http-intake.logs.datadoghq.com/api/v2/logs" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -d @logs.json`

**Examples:**
- curl -X POST "https://http-intake.logs.datadoghq.com/api/v2/logs" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -d @logs.json
- curl -s -X POST "https://api.datadoghq.com/api/v2/logs/events/search" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d '{"filter":{"query":"service:checkout duration:>500"}}' | jq '.meta.page'
- curl -s -X POST "https://api.datadoghq.com/api/v2/logs/events/aggregate" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d '{"compute":[{"aggregation":"count"}],"group_by":[{"facet":"status"}]}' | jq '.data.buckets'

### log-pipelines
Manage log processing pipelines, processors, and indexes via the Logs Configuration API

**Commands:**
- `curl -X GET "https://api.datadoghq.com/api/v1/logs/config/pipelines" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"`
- `curl -X POST "https://api.datadoghq.com/api/v1/logs/config/pipelines" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d @pipeline.json`
- `curl -X DELETE "https://api.datadoghq.com/api/v1/logs/config/pipelines/PIPELINE_ID" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"`
- `curl -X GET "https://api.datadoghq.com/api/v1/logs/config/indexes" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"`

**Examples:**
- curl -X POST "https://api.datadoghq.com/api/v1/logs/config/pipelines" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d '{"name":"Parse Nginx","filter":{"query":"source:nginx"}}'
- curl -X GET "https://api.datadoghq.com/api/v1/logs/config/pipelines" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" | jq '.pipelines[].name'
- curl -X DELETE "https://api.datadoghq.com/api/v1/logs/config/pipelines/abc123" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"
