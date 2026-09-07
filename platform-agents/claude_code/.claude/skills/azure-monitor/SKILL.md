---
name: "azure-monitor"
description: "Collects and evaluates Azure resource metrics and alerts via the Azure CLI: retrieves metric time series, defines metric and activity log alert rules with conditions, manages action groups, and queries the activity log for operational auditing. Use when working with metrics, alerts, activity log, api or when the user mentions metrics, alerts, activity log, api."
license: "MIT"
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(az:*)"
---

Collects and evaluates Azure resource metrics and alerts via the Azure CLI: retrieves metric time series, defines metric and activity log alert rules with conditions, manages action groups, and queries the activity log for operational auditing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `az monitor metrics list --resource /subscriptions/12345678-1`, `az monitor alert create --name api-5xx --resource-group api-`
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

# Azure Monitor

## What this skill does

Collects and evaluates Azure resource metrics and alerts via the Azure CLI: retrieves metric time series, defines metric and activity log alert rules with conditions, manages action groups, and queries the activity log for operational auditing.

## When to use

- Checking an API's request count or latency trend
- Creating an alert for a new resource
- Auditing failed operations

## Real commands

```bash
# List available metrics
az monitor metrics list-definitions --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api

# Retrieve a metric for a day
az monitor metrics list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --metric-names Requests --start-time 2026-08-01T00:00:00Z --end-time 2026-08-01T23:59:59Z --interval PT1H

# Create an alert
az monitor alert create --name api-5xx --resource-group api-rg --condition "percentage CPU > 90 avg 5m" --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api

# List alerts
az monitor alert list --resource-group api-rg --query '[].{name:name,severity:severity}' -o table

# Activity log failures
az monitor activity-log list --status Failed --max-events 20
```

## Testing

- Trigger an alert condition intentionally and confirm firing state
- Verify action group notifications arrive

## Best practices

- Use App Insights queries for application-level metrics
- Aggregate alerts per resource group for manageability
- Set action groups with escalation paths

## Capabilities

### metrics
Retrieve resource metrics and definitions.

**Parameters:**
- `resource_id` (string): Azure resource ID
- `metric_names` (string): Metric names
- `interval` (string): Time granularity (PT1H, PT5M)

**Commands:**
- `az monitor metrics list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --metric-names Requests`
- `az monitor metrics list-definitions --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api`
- `az monitor metrics list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --metric-names Requests --start-time 2026-08-01T00:00:00Z --end-time 2026-08-01T23:59:59Z --interval PT1H`
- `az monitor metrics list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --metric-names Requests --aggregation count --top 5`

**Examples:**
- az monitor metrics list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --metric-names "Requests" "5XX" --start-time $(date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --interval PT6H
- az monitor metrics list-definitions --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --query '[].{name:name.value}' -o table
- az monitor metrics list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --metric-names Percentage CPU --aggregation average

### alerts
Create and manage metric/activity alerts.

**Parameters:**
- `condition` (string): Alert condition string
- `severity` (number): 0-4 severity
- `action_group` (string): Action group ID

**Commands:**
- `az monitor alert create --name api-5xx --resource-group api-rg --condition "percentage CPU > 90 avg 5m" --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api`
- `az monitor alert list --resource-group api-rg`
- `az monitor alert show --name api-5xx -g api-rg`
- `az monitor alert update --name api-5xx -g api-rg --condition "percentage CPU > 95 avg 5m"`
- `az monitor alert delete --name api-5xx -g api-rg`

**Examples:**
- az monitor alert create --name api-latency --resource-group api-rg --condition "Avg Requests Duration > 5000 avg 5m" --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Insights/components/my-insights --action /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Insights/actionGroups/my-ag
- az monitor alert list --resource-group api-rg --query '[].{name:name,severity:severity}' -o table
- az monitor alert create --name vm-down --resource-group api-rg --condition "All VM sizes - count > 0" --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Compute/virtualMachines/my-vm

### activity-log
Query the activity log.

**Parameters:**
- `status` (string): Filter by status (Failed, Succeeded)
- `max_events` (number): Max events to return

**Commands:**
- `az monitor activity-log list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api`
- `az monitor activity-log list --status Failed --max-events 20`
- `az monitor activity-log list --resource-group api-rg --start-time 2026-08-01 --end-time 2026-08-02`
- `az monitor activity-log list --category Administrative --query '[].{time:eventTimestamp,op:operationName.value}' -o table`

**Examples:**
- az monitor activity-log list --status Failed --max-events 50 | jq '.[].operationName.value'
- az monitor activity-log list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-api --query '[].{t:eventTimestamp,o:operationName.value}' -o table
- az monitor activity-log list --resource-group api-rg --start-time 2026-08-01T00:00:00Z --max-events 10

## References
- [Azure Monitor Docs](https://learn.microsoft.com/en-us/azure/azure-monitor/)
- [Azure CLI monitor Reference](https://learn.microsoft.com/en-us/cli/azure/monitor)
