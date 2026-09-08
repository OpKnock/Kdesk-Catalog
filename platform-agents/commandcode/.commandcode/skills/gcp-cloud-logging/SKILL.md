---
name: "gcp-cloud-logging"
description: "GCP Cloud Logging operations: query logs with gcloud logging read, create log-based metrics, and export logs to storage sinks. Use when working with gcp logging, api or when the user mentions gcp logging, api."
license: "MIT"
compatibility: "Requires gcloud."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(gcloud:*)"
---

GCP Cloud Logging operations: query logs with gcloud logging read, create log-based metrics, and export logs to storage sinks.

## Agentic Workflow: Read -> Reason -> Act (gcp-cloud-logging)

You are **Gcp Cloud Logging** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gcp-cloud-logging`
- Domain: GCP Cloud Logging operations: query logs with gcloud logging read, create log-based metrics, and export logs to storage sinks.
- **gcp-logging**: Read logs, create log-based metrics, and manage exports. — `gcloud logging read 'resource.type=cloud_run_revision AND severity>=ERROR' --lim`
- Check `knowledge` and `prerequisites: gcloud`

### 2. Reason — think for `gcp-cloud-logging`
- For `gcp-logging`: Read logs, create log-based metrics, and manage exports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gcp-cloud-logging` tools
- Tools: `Glob`, `Grep`, `Read`, `Gcloud` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gcp-cloud-logging:946232c5`

# GCP Cloud Logging

## What this skill does

Cloud Logging aggregates logs from GCP services. gcloud logging read filters and returns entries; metrics turn filters into counters for dashboards; sinks export to Storage/BigQuery.

## When to use

- Debugging errors across Cloud Run/Functions/VM services
- Building error-rate metrics for SLOs
- Archiving logs for compliance

## Real commands

```bash
# Read recent errors
 gcloud logging read 'resource.type=cloud_run_revision AND severity>=ERROR' --limit=50 --format='table(timestamp,severity,jsonPayload.message)'

# Recent request logs
 gcloud logging read 'logName=projects/my-project/logs/requests' --freshness=1d --limit=20

# Stream live
 gcloud logging tail 'severity=ERROR'

# Log-based metric
 gcloud logging metrics create 5xx-errors --description='5xx rate' --filter='resource.type=global AND httpRequest.status>=500'

# Export sink
 gcloud logging sinks create archive-errors storage.googleapis.com --log-filter='severity>=ERROR'
```

## Structured logging (Python example)

```python
import json, sys
print(json.dumps({"message": "order failed", "severity": "ERROR", "orderId": oid}))
```

## Testing

```bash
# Trigger an error, then confirm it is searchable
 gcloud logging read 'jsonPayload.orderId="1"' --freshness=10m --limit=5
```

## Best practices

- Emit structured JSON logs so filters can target fields.
- Add `trace` fields to correlate with Cloud Trace.
- Use log-based metrics for SLO counters instead of scraping logs.
- Set sink filters tight; archiving everything costs storage.
- Prefer `--format='table(...)'` for human-readable triage output.

## Capabilities

### gcp-logging
Read logs, create log-based metrics, and manage exports.

**Parameters:**
- `filter` (string): Logging filter expression
- `limit` (integer): Number of entries to return
- `sink-name` (string): Log sink name for exports

**Commands:**
- `gcloud logging read 'resource.type=cloud_run_revision AND severity>=ERROR' --limit=50 --format='table(timestamp,severity,jsonPayload.message)'`
- `gcloud logging read 'logName=projects/my-project/logs/requests' --freshness=1d --limit=20`
- `gcloud logging metrics create 5xx-errors --description='5xx rate' --filter='resource.type=global AND httpRequest.status>=500'`
- `gcloud logging metrics describe 5xx-errors`
- `gcloud logging sinks create archive-errors storage.googleapis.com --log-filter='severity>=ERROR'`
- `gcloud logging tail 'severity=ERROR'`

**Examples:**
- gcloud logging read 'resource.type=cloud_run_revision AND severity>=ERROR' --limit=50 --format='table(timestamp,severity,jsonPayload.message)'
- gcloud logging metrics create 5xx-errors --description='5xx rate' --filter='resource.type=global AND httpRequest.status>=500'
- gcloud logging tail 'severity=ERROR'

## References
- [Cloud Logging docs](https://cloud.google.com/logging/docs)
- [gcloud logging reference](https://cloud.google.com/sdk/gcloud/reference/logging)
