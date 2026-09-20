---
name: "cost-azure"
description: "Tracks Azure cloud spend with Cost Management queries, exports, budgets, and consumption APIs to keep billing under control."
---

# Cost Azure

Tracks Azure cloud spend with Cost Management queries, exports, budgets, and consumption APIs to keep billing under control.

## Instructions

# Azure Cost Optimization

Understand and reduce Azure spend with Cost Management CLI queries.

## When to Use

- Monthly cost analysis per resource group or service
- Setting budget alerts for subscriptions
- Automating cost data exports to storage for BI
- Spotting VM overspend before invoice day

## Query cost

```bash
az cost-management query --type ActualCost --timeframe MonthToDate --scope /subscriptions/$SUBSCRIPTION_ID --aggregation '{"totalCost":{"name":"PreTaxCost","function":"Sum"}}'
```

Group by dimension for a breakdown:

```bash
az cost-management query --type ActualCost --timeframe LastMonth --scope /subscriptions/$SUB --grouping '{"type":"Dimension","name":"ServiceName"}'
```

## Budgets

```bash
az consumption budget create --budget-name eng-monthly --amount 15000 --time-grain monthly --start-date 2026-08-01
```

Attach action groups so budget thresholds page the FinOps on-call.

## Exports to storage

```bash
az cost-management export create --name monthly-export --type ActualCost --timeframe MonthToDate --storage-account $SA --container $CONTAINER --scope /subscriptions/$SUB
az cost-management export run --name monthly-export --scope /subscriptions/$SUB
```

## VM rightsizing

Check actual utilization before resizing:

```bash
az monitor metrics list --resource $RESOURCE_ID --metric PercentageCPU --interval PT1H
```

## Best practices

- Always scope queries to the subscription, not the tenant root.
- Set budgets at 80% and 100% of forecast spend.
- Export daily Parquet files to a lake and aggregate there.
- Apply Azure Hybrid Benefit for Windows/Linux VMs before paying on-demand.

## Capabilities

### cost-management
Query Azure cost data and manage exports via az cost-management.

**Commands:**
- `az cost-management query --type ActualCost --timeframe MonthToDate --scope /subscriptions/$SUBSCRIPTION_ID --aggregation '{"totalCost":{"name":"PreTaxCost","function":"Sum"}}'`
- `az cost-management query --type ActualCost --timeframe LastMonth --scope /subscriptions/$SUBSCRIPTION_ID --grouping '{"type":"Dimension","name":"ServiceName"}'`
- `az cost-management export create --name monthly-export --type ActualCost --timeframe MonthToDate --storage-account $SA --container $CONTAINER --scope /subscriptions/$SUBSCRIPTION_ID`
- `az cost-management export list --scope /subscriptions/$SUBSCRIPTION_ID`
- `az cost-management export run --name monthly-export --scope /subscriptions/$SUBSCRIPTION_ID`

**Examples:**
- az cost-management query --type ActualCost --timeframe LastMonth --scope /subscriptions/$SUB --grouping '{"type":"Dimension","name":"ResourceGroupName"}'
- az cost-management query --type ActualCost --timeframe MonthToDate --scope /subscriptions/$SUB --aggregation '{"totalCost":{"name":"PreTaxCost","function":"Sum"}}'
- az cost-management export create --name daily-export --type ActualCost --timeframe MonthToDate --storage-account sa --container cost

### budgets
Create Azure budgets and view consumption data.

**Commands:**
- `az consumption budget create --budget-name engineering-monthly --amount 15000 --time-grain monthly --start-date 2026-08-01 --category cost`
- `az consumption budget list`
- `az consumption budget show --budget-name engineering-monthly`
- `az consumption usage list --top 10 --metric usage`
- `az monitor metrics list --resource $RESOURCE_ID --metric PercentageCPU --interval PT1H`

**Examples:**
- az consumption budget create --budget-name eng-monthly --amount 15000 --time-grain monthly --start-date 2026-08-01
- az consumption usage list --top 20 | jq '.[] | {name: .name.value, quantity: .quantity}'
- az consumption budget show --budget-name eng-monthly
