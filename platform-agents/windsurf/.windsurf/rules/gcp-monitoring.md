---
trigger: glob
description: "GCP Cloud Monitoring operations: query metric time series, create alerting policies, and check uptime from the gcloud CLI. Use when working with gcp monitoring, api or when the user mentions gcp monitoring, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

GCP Cloud Monitoring operations: query metric time series, create alerting policies, and check uptime from the gcloud CLI.

## Agentic Workflow: Read -> Reason -> Act (gcp-monitoring)

You are **Gcp Monitoring** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gcp-monitoring`
- Domain: GCP Cloud Monitoring operations: query metric time series, create alerting policies, and check uptime from the gcloud CLI.
- **gcp-monitoring**: Query metrics, manage alerting policies, and verify uptime checks. — `gcloud monitoring time-series list --filter='metric.type="run.googleapis.com/req`
- Check `knowledge` and `prerequisites: gcloud`

### 2. Reason — think for `gcp-monitoring`
- For `gcp-monitoring`: Query metrics, manage alerting policies, and verify uptime checks. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gcp-monitoring` tools
- Tools: `Glob`, `Grep`, `Read`, `Gcloud` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gcp-monitoring:e435a876`

# GCP Monitoring

## What this skill does

Cloud Monitoring collects metrics from GCP services and custom agents. The gcloud CLI lists time series, creates alerting policies and notification channels, and manages uptime checks.

## When to use

- Verifying a service emits expected metrics
- Creating alerts for SLO violations
- Adding synthetic uptime checks to external endpoints

## Real commands

```bash
# Query request counts by response code
 gcloud monitoring time-series list --filter='metric.type="run.googleapis.com/request_count" AND resource.labels.service_name="orders"' --format='table(metric.labels.response_code, pointCount)'

# Notification channel
 gcloud monitoring channels create --display-name=ops-email --type=email --channel-labels=address=oncall@example.com

# Alerting policy
 gcloud monitoring policies create --display-name='5xx high' --condition-filter='metric.type="run.googleapis.com/request_count" AND metric.labels.response_code="500"' --duration=300s

# Uptime check
 gcloud monitoring uptime-checks create --display-name=orders --resource-type=url --resource-url=https://orders.example.com/health --timeout=5s
```

## Custom metric ingestion

```bash
# Push a custom counter from a VM
curl -s -X POST https://monitoring.googleapis.com/v3/projects/my-project/timeSeries -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d @ts.json | jq
```

## Testing

```bash
# Confirm an alert fires: stop the service, wait 5m, list incidents
 gcloud monitoring incidents list --filter='policy.displayName="5xx high"' --freshness=1d | jq '.incidents | length'
```

## Best practices

- Alert on error budgets and burn rate, not raw metrics.
- Attach channels (email, PagerDuty) at policy creation.
- Use uptime checks for external endpoints; keep timeouts small.
- Pin metric types to documented descriptors (check the UI for typos).
- Prefer `--format=json` + jq when scripting metric queries.

## Capabilities

### gcp-monitoring
Query metrics, manage alerting policies, and verify uptime checks.

**Parameters:**
- `metric-type` (string): Metric descriptor like run.googleapis.com/request_count
- `filter` (string): Time series filter expression
- `duration` (string): Alert condition duration like 300s

**Commands:**
- `gcloud monitoring time-series list --filter='metric.type="run.googleapis.com/request_count" AND resource.labels.service_name="orders"' --format='table(metric.labels.response_code, pointCount)'`
- `gcloud monitoring time-series list --filter='metric.type="cloudfunctions.googleapis.com/function/execution_times"' --format='json' | jq '.timeSeries[0].points[0].value'`
- `gcloud monitoring channels create --display-name=ops-email --type=email --channel-labels=address=oncall@localhost`
- `gcloud monitoring policies create --display-name='5xx high' --condition-filter='metric.type="run.googleapis.com/request_count" AND metric.labels.response_code="500"' --duration=300s`
- `gcloud monitoring uptime-checks create --display-name=orders --resource-type=url --resource-url=http://localhost:8080/health --timeout=5s`

**Examples:**
- gcloud monitoring time-series list --filter='metric.type="run.googleapis.com/request_count" AND resource.labels.service_name="orders"' --format='table(metric.labels.response_code, pointCount)'
- gcloud monitoring channels create --display-name=ops-email --type=email --channel-labels=address=oncall@localhost
- gcloud monitoring uptime-checks create --display-name=orders --resource-type=url --resource-url=http://localhost:8080/health --timeout=5s

## References
- [Cloud Monitoring docs](https://cloud.google.com/monitoring/docs)
- [gcloud monitoring reference](https://cloud.google.com/sdk/gcloud/reference/monitoring)
