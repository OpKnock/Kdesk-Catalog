---
type: agent_requested
description: "Manages GCP billing accounts, budgets, and BigQuery billing exports using gcloud and bq to control cloud spend. Use when working with billing, budgets, cost gcp or when the user mentions billing, budgets, cost gcp."
---

Manages GCP billing accounts, budgets, and BigQuery billing exports using gcloud and bq to control cloud spend.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gcloud billing accounts list`, `gcloud billing budgets create --billing-account=$BILLING_ACC`
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

# GCP Cost Optimization

Control Google Cloud spend via billing accounts, budgets, and BigQuery exports.

## When to Use

- Auditing which projects are linked to which billing accounts
- Enforcing budget alerts for teams and products
- Analyzing cost with BigQuery billing exports
- Cleaning up orphaned projects that still bill

## Billing accounts

```bash
gcloud billing accounts list
gcloud billing projects link my-app-prod --billing-account 012345-67890A-BCDEFG
```

Never link a production project to a sandbox billing account - always verify with `gcloud billing projects describe`.

## Budgets

```bash
gcloud billing budgets create --billing-account=012345-67890A-BCDEFG --display-name=eng-monthly --budget-amount=15000 --threshold-rule=percent=80 --threshold-rule=percent=100
```

## BigQuery export analysis

With billing export enabled, query costs by service and label:

```sql
SELECT service.description, SUM(cost) AS total
FROM `billing_dataset.gcp_billing_export_v1`
WHERE invoice.month = '202607'
GROUP BY service.description
ORDER BY total DESC
```

```bash
bq query --use_legacy_sql=false "SELECT service.description, SUM(cost) AS total FROM \`billing_dataset.gcp_billing_export_v1\` WHERE invoice.month='202607' GROUP BY service.description ORDER BY total DESC"
```

## Best practices

- Enforce labels (`team`, `env`, `app`) and include them in budgets with `--filter`.
- Use committed use discounts for stable workloads.
- Review BigQuery export monthly and archive to cheaper storage.
- Set budget notifications to Slack via pub/sub before the threshold hits.

## Testing

```bash
gcloud billing budgets list --billing-account=012345-67890A-BCDEFG
```

Confirm budget state after each create/update.

## Capabilities

### billing
Manage GCP billing accounts and project linkage with gcloud billing.

**Parameters:**
- `billing-account` (string): Billing account id in XXXXXX-XXXXXX-XXXXXX format
- `project` (string): GCP project id to link or query
- `format` (string): gcloud output format: table, json, csv

**Commands:**
- `gcloud billing accounts list`
- `gcloud billing projects describe $PROJECT_ID`
- `gcloud billing projects link $PROJECT_ID --billing-account $BILLING_ACCOUNT_ID`
- `gcloud billing accounts describe $BILLING_ACCOUNT_ID`
- `gcloud billing projects unlink $PROJECT_ID`

**Examples:**
- gcloud billing accounts list --format='table(displayName,open,masterBillingAccount)'
- gcloud billing projects link my-app-prod --billing-account 012345-67890A-BCDEFG
- gcloud billing projects describe my-app-prod

### budgets
Create and monitor GCP budget thresholds.

**Parameters:**
- `budget-amount` (number): Budget amount in USD
- `threshold-rule` (string): percent=N or absolute amount alerts, repeatable
- `display-name` (string): Human-readable budget name

**Commands:**
- `gcloud billing budgets create --billing-account=$BILLING_ACCOUNT_ID --display-name=eng-monthly --budget-amount=15000 --threshold-rule=percent=80 --threshold-rule=percent=100`
- `gcloud billing budgets list --billing-account=$BILLING_ACCOUNT_ID`
- `gcloud billing budgets describe eng-monthly --billing-account=$BILLING_ACCOUNT_ID`
- `gcloud billing budgets update eng-monthly --billing-account=$BILLING_ACCOUNT_ID --budget-amount=18000`
- `gcloud billing budgets delete eng-monthly --billing-account=$BILLING_ACCOUNT_ID`

**Examples:**
- gcloud billing budgets create --billing-account=012345-67890A-BCDEFG --display-name=eng --budget-amount=15000 --threshold-rule=percent=80
- gcloud billing budgets list --billing-account=012345-67890A-BCDEFG --format='table(displayName,budgetFilter.creditTypesTreatment,amount)'
- gcloud billing budgets describe eng --billing-account=012345-67890A-BCDEFG

## References
- [GCP Billing Docs](https://cloud.google.com/billing/docs)
- [gcloud billing reference](https://cloud.google.com/sdk/gcloud/reference/billing)
- [Billing export to BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery)