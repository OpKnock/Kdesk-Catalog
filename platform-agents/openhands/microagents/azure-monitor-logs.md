---
name: "azure-monitor-logs"
description: "Queries and administers Log Analytics workspaces with the Azure CLI: creates workspaces, runs KQL queries for application and audit diagnostics, and configures diagnostic settings to route resource logs."
type: knowledge
triggers: ["azure-monitor-logs", "workspaces", "kql-queries", "diagnostic-settings"]
---

# Azure Monitor Logs

Queries and administers Log Analytics workspaces with the Azure CLI: creates workspaces, runs KQL queries for application and audit diagnostics, and configures diagnostic settings to route resource logs.

## Instructions

# Azure Monitor Logs

## What this skill does

Queries and administers Log Analytics workspaces with the Azure CLI: creates workspaces, runs KQL queries for application and audit diagnostics, and configures diagnostic settings to route resource logs.

## When to use

- Investigating 500s across an app with AppRequests/AppExceptions
- Auditing activity via AzureActivity queries
- Enabling log collection for a resource

## Real commands

```bash
# Create a workspace
az monitor log-analytics workspace create -g rg -n myworkspace

# Query app errors
az monitor log-analytics query -w <workspace-id> --analytics-query "AppRequests | where Success == false | summarize count() by bin(TimeGenerated, 1h)"

# Query activity log
az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AzureActivity | where OperationName contains 'write' | take 20"

# Enable diagnostics for Key Vault
az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --workspace abc123-def456-ghi789 --logs '[{"category":"AuditEvent","enabled":true}]'
```

## Testing

- Run a small KQL query first, then expand filters
- Verify diagnostic settings with az monitor diagnostic-settings list

## Best practices

- Set retention to match compliance needs
- Use summarize by bin(TimeGenerated, 1h) to reduce noise
- Send only required categories to control cost

## Capabilities

### workspaces
Create and manage Log Analytics workspaces.

**Commands:**
- `az monitor log-analytics workspace create -g rg -n myworkspace`
- `az monitor log-analytics workspace list`
- `az monitor log-analytics workspace show -g rg -n myworkspace --query 'customerId' -o tsv`
- `az monitor log-analytics workspace delete -g rg -n myworkspace --yes`
- `az monitor log-analytics workspace update -g rg -n myworkspace --retention-time 90`

**Examples:**
- az monitor log-analytics workspace create -g rg -n myworkspace --sku PerGB2018
- az monitor log-analytics workspace show -g rg -n myworkspace --query 'id' -o tsv
- az monitor log-analytics workspace update -g rg -n myworkspace --retention-time 180

### kql-queries
Run Kusto queries against workspaces.

**Commands:**
- `az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AzureDiagnostics | where OperationName contains 'error' | take 10"`
- `az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AppRequests | where Success == false | summarize count() by bin(TimeGenerated, 1h)"`
- `az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AzureActivity | where OperationName == 'Microsoft.Compute/virtualMachines/write' | take 20"`
- `az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "Heartbeat | summarize count() by Computer"`

**Examples:**
- az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AppRequests | where ResultCode == 500 | summarize count() by bin(TimeGenerated, 1h) | order by TimeGenerated desc"
- az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AzureDiagnostics | where Category == 'AuditLogs' | take 5"
- az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AppExceptions | project TimeGenerated, Message | take 20"

### diagnostic-settings
Route resource logs to workspaces.

**Commands:**
- `az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --workspace abc123-def456-ghi789 --logs '[{"category":"AuditLogs","enabled":true}]'`
- `az monitor diagnostic-settings list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv`
- `az monitor diagnostic-settings update --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --name settings --logs '[{"category":"AuditLogs","enabled":false}]'`
- `az monitor diagnostic-settings delete --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --name settings`

**Examples:**
- az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --workspace abc123-def456-ghi789 --logs '[{"category":"AuditEvent","enabled":true}]'
- az monitor diagnostic-settings list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --query '[].{name:name,workspaceId:workspaceId}' -o table
- az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-func --workspace abc123-def456-ghi789 --metrics '[{"category":"AllMetrics","enabled":true}]'
