---
name: "sumologic"
description: "Ingest logs and run queries against Sumo Logic using HTTP collectors and the REST API. Pushes JSON events directly, starts search jobs with SPL-style syntax, fetches results, and manages collectors \u2014 all from the terminal without a collector agent. Use when working with sumologic api or when the user mentions sumologic api."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*)"
---

Ingest logs and run queries against Sumo Logic using HTTP collectors and the REST API. Pushes JSON events directly, starts search jobs with SPL-style syntax, fetches results, and manages collectors — all from the terminal without a collector agent.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST 'https://collectors.sumologic.com/receiver/v1/h`
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

**Parameters:**
- `query` (string): Sumo Logic query with SPL-style pipes
- `from` (string): Start of time range, e.g. -1h
- `http_source_url` (string): HTTP collector source URL (URL-encoded)

**Commands:**
- `curl -X POST 'https://collectors.sumologic.com/receiver/v1/http/$HTTP_SOURCE_URL_ENCODED' -H 'Content-Type: application/json' -d '{"event":"payment.completed","account":42}'`
- `curl -s -X POST 'https://api.sumologic.com/api/v1/search/jobs' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" -H 'Content-Type: application/json' -d '{"query":"_sourceCategory=api ERROR | count by _sourceHost","from":"-1h","to":"now"}'`
- `curl -s 'https://api.sumologic.com/api/v1/search/jobs/$JOB_ID/results' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" -H 'Accept: application/json'`
- `curl -s 'https://api.sumologic.com/api/v1/collectors' -u "$SUMOLOGIC_ACCESS_ID:$SUMOLOGIC_ACCESS_KEY" | jq '.collectors[].name'`

**Examples:**
- curl -X POST 'https://collectors.sumologic.com/receiver/v1/http/$HTTP_SOURCE_URL_ENCODED' -H 'Content-Type: application/json' -d '{"event":"order.created","order_id":7}'
- curl -s -X POST 'https://api.sumologic.com/api/v1/search/jobs' -u "$ID:$KEY" -d '{"query":"_sourceCategory=api status>=500 | count by host","from":"-15m","to":"now"}'
- curl -s 'https://api.sumologic.com/api/v1/collectors' -u "$ID:$KEY" | jq '.collectors | length'

## References
- [Sumo Logic docs](https://help.sumologic.com/docs/)
- [HEC-style HTTP Source](https://help.sumologic.com/docs/send-data/hosted-collectors/http-source/)
