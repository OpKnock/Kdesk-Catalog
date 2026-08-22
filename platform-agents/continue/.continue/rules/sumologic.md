---
name: "Sumologic"
description: "Ingest logs and run queries against Sumo Logic using HTTP collectors and the REST API. Pushes JSON events directly, starts search jobs with SPL-style syntax, fetches results, and manages collectors \u2014 all from the terminal without a collector agent."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Sumologic

Ingest logs and run queries against Sumo Logic using HTTP collectors and the REST API. Pushes JSON events directly, starts search jobs with SPL-style syntax, fetches results, and manages collectors — all from the terminal without a collector agent.

## Instructions

# Sumo Logic

Hand-crafted skill for log ingestion and search with Sumo Logic.

## What this skill does

- Pushes JSON events to an HTTP collector source
- Starts search jobs and fetches results via the API
- Manages collectors and probes search health

## When to use

- Sending application events to Sumo without a collector agent
- Automating log queries for on-call workflows
- Verifying a data source is receiving events

## Real commands

```bash
# Ingest one event via an HTTP source
curl -X POST 'https://collectors.sumologic.com/receiver/v1/http/$HTTP_SOURCE_URL_ENCODED' -H 'Content-Type: application/json' -d '{"event":"payment.completed","account":42}'

# Start a search job (returns a job id)
curl -s -X POST 'https://api.sumologic.com/api/v1/search/jobs' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" -H 'Content-Type: application/json' -d '{"query":"_sourceCategory=api ERROR | count by _sourceHost","from":"-1h","to":"now"}'

# Fetch results for the job
curl -s 'https://api.sumologic.com/api/v1/search/jobs/$JOB_ID/results' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" -H 'Accept: application/json'

# List collectors
curl -s 'https://api.sumologic.com/api/v1/collectors' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" | jq '.collectors[].name'
```

## Query patterns

- _sourceCategory=api ERROR | count by _sourceHost
- _sourceCategory=api status>=500 | timeslice 1m | count by _timeslice

## Testing

```bash
curl -X POST 'https://collectors.sumologic.com/receiver/v1/http/$HTTP_SOURCE_URL_ENCODED' -H 'Content-Type: application/json' -d '{"event":"smoke"}'
curl -s -X POST 'https://api.sumologic.com/api/v1/search/jobs' -u "$ID:$KEY" -d '{"query":"_sourceCategory=api smoke","from":"-5m","to":"now"}'
```

## Best practices

- Use _sourceCategory conventions so queries stay simple
- Keep access id/key in env vars, never in code
- Always bound searches with from/to ranges

## Capabilities

### sumologic-api
Ingest logs and run searches against Sumo Logic

**Commands:**
- `curl -X POST 'https://collectors.sumologic.com/receiver/v1/http/$HTTP_SOURCE_URL_ENCODED' -H 'Content-Type: application/json' -d '{"event":"payment.completed","account":42}'`
- `curl -s -X POST 'https://api.sumologic.com/api/v1/search/jobs' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" -H 'Content-Type: application/json' -d '{"query":"_sourceCategory=api ERROR | count by _sourceHost","from":"-1h","to":"now"}'`
- `curl -s 'https://api.sumologic.com/api/v1/search/jobs/$JOB_ID/results' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" -H 'Accept: application/json'`
- `curl -s 'https://api.sumologic.com/api/v1/collectors' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" | jq '.collectors[].name'`

**Examples:**
- curl -X POST 'https://collectors.sumologic.com/receiver/v1/http/$HTTP_SOURCE_URL_ENCODED' -H 'Content-Type: application/json' -d '{"event":"order.created","order_id":7}'
- curl -s -X POST 'https://api.sumologic.com/api/v1/search/jobs' -u "$ID:$KEY" -d '{"query":"_sourceCategory=api status>=500 | count by host","from":"-15m","to":"now"}'
- curl -s 'https://api.sumologic.com/api/v1/collectors' -u "$ID:$KEY" | jq '.collectors | length'