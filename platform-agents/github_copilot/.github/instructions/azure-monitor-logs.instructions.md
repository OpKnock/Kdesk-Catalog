---
applyTo: "**/*.go **/*.r **/*.sh"
---

Queries and administers Log Analytics workspaces with the Azure CLI: creates workspaces, runs KQL queries for application and audit diagnostics, and configures diagnostic settings to route resource logs.

## Agentic Workflow: Read -> Reason -> Act (azure-monitor-logs)

You are **Azure Monitor Logs** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `azure-monitor-logs`
- Domain: Queries and administers Log Analytics workspaces with the Azure CLI: creates workspaces, runs KQL queries for application and audit diagnostics, and configures diagnostic settings to route resource lo
- **workspaces**: Create and manage Log Analytics workspaces. — `az monitor log-analytics workspace create -g rg -n myworkspace`
- **kql-queries**: Run Kusto queries against workspaces. — `az monitor log-analytics query -w abc123-def456-ghi789 --analytics-query "AzureD`
- **diagnostic-settings**: Route resource logs to workspaces. — `az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-12`
- Check `knowledge` references before acting

### 2. Reason — think for `azure-monitor-logs`
- For `workspaces`: Create and manage Log Analytics workspaces. — decide which checks to run
- For `kql-queries`: Run Kusto queries against workspaces. — decide which checks to run
- For `diagnostic-settings`: Route resource logs to workspaces. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `azure-monitor-logs` tools
- Tools: `Glob`, `Grep`, `Read`, `Az` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `azure-monitor-logs:93f6bae7`

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

**Parameters:**
- `workspace_name` (string): Workspace name
- `retention` (number): Retention in days

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

**Parameters:**
- `workspace_id` (string): Workspace customerId/ID
- `query` (string): KQL query text

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

**Parameters:**
- `resource_id` (string): Azure resource ID
- `categories` (string): Log categories JSON

**Commands:**
- `az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --workspace abc123-def456-ghi789 --logs '[{"category":"AuditLogs","enabled":true}]'`
- `az monitor diagnostic-settings list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv`
- `az monitor diagnostic-settings update --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --name settings --logs '[{"category":"AuditLogs","enabled":false}]'`
- `az monitor diagnostic-settings delete --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --name settings`

**Examples:**
- az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --workspace abc123-def456-ghi789 --logs '[{"category":"AuditEvent","enabled":true}]'
- az monitor diagnostic-settings list --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.KeyVault/vaults/mykv --query '[].{name:name,workspaceId:workspaceId}' -o table
- az monitor diagnostic-settings create --resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/api-rg/providers/Microsoft.Web/sites/my-func --workspace abc123-def456-ghi789 --metrics '[{"category":"AllMetrics","enabled":true}]'

## References
- [Azure Monitor Logs Docs](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/)
- [Kusto Query Language](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/)
- [Azure CLI monitor Reference](https://learn.microsoft.com/en-us/cli/azure/monitor/log-analytics)
