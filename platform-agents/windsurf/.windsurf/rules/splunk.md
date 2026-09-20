---
trigger: glob
description: "Drives log analysis and event ingestion in Splunk: runs bounded SPL queries, registers file monitor inputs, and pushes structured events through HTTP Event Collector and REST search endpoints."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Splunk

Drives log analysis and event ingestion in Splunk: runs bounded SPL queries, registers file monitor inputs, and pushes structured events through HTTP Event Collector and REST search endpoints.

## Instructions

# Splunk

Drives log analysis and event ingestion in Splunk.

## What this skill does

- Runs SPL searches from the CLI with time and stats clauses
- Adds file monitors as data inputs
- Ingests JSON events via HTTP Event Collector and queries via REST

## When to use

- Digging into errors across a fleet of hosts
- Onboarding a new application log file
- Automating searches for dashboards and alerts

## Real commands

```bash
# Start the platform (first run)
./splunk start --accept-license

# Search
splunk search "index=_internal level=ERROR earliest=-1h | stats count by sourcetype"

# Top error sources
splunk search "index=_internal ERROR | top sourcetype"

# Monitor a log file
splunk add monitor /var/log/api.log -index main -sourcetype api_logs

# REST: run a search job
curl -k -u admin:changeme 'https://localhost:8089/services/search/jobs' -d 'search=index=main status>=500 earliest=-15m&output_mode=json'

# HEC: push an event
curl -k -X POST 'https://localhost:8088/services/collector/event' -H "Authorization: Splunk $HEC_TOKEN" -d '{"event":"api started","sourcetype":"api_events"}'
```

## SPL patterns

- index=main sourcetype=access_combined status>=500
- | timechart count by status
- | stats avg(latency) by host

## Testing

```bash
curl -k -X POST 'https://localhost:8088/services/collector/event' -H "Authorization: Splunk $HEC_TOKEN" -d '{"event":"smoke","sourcetype":"api_events"}'
splunk search "index=main sourcetype=api_events earliest=-5m"
```

## Best practices

- Always bound searches with earliest/latest
- Give every app its own sourcetype for parsing rules
- Use HEC tokens scoped per index for production ingestion

## Capabilities

### splunk-search-ingest
Runs SPL queries, configures data inputs, and pushes events through HEC and REST endpoints

**Commands:**
- `./splunk start --accept-license`
- `splunk search "index=_internal level=ERROR earliest=-1h | stats count by sourcetype"`
- `splunk add monitor /var/log/api.log -index main -sourcetype api_logs`
- `curl -k -u admin:changeme 'https://localhost:8089/services/search/jobs' -d 'search=index=main status>=500 earliest=-15m&output_mode=json'`
- `curl -k -X POST 'https://localhost:8088/services/collector/event' -H "Authorization: Splunk $HEC_TOKEN" -d '{"event":"api started","sourcetype":"api_events"}'`

**Examples:**
- splunk search "index=_internal ERROR | top sourcetype"
- splunk add monitor /var/log/api.log -index main -sourcetype api_logs
- curl -k -X POST 'https://localhost:8088/services/collector/event' -H "Authorization: Splunk $HEC_TOKEN" -d '{"event":"test"}'
