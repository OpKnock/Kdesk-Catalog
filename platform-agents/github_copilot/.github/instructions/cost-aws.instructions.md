---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Analyzes and reduces AWS spend with Cost Explorer, Budgets, Compute Optimizer, and Cost Optimization Hub CLI queries.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aws ce get-cost-and-usage --time-period Start=2026-07-01,End`, `aws cost-optimization-hub list-recommendations --category Co`
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

# AWS Cost Optimization

Find and eliminate AWS waste using native Cost Explorer and optimization APIs.

## When to Use

- Monthly cost review by service or team
- Detecting spend anomalies before they compound
- Rightsizing EC2, RDS, and EBS resources
- Validating reservations and Savings Plans coverage

## Cost exploration

```bash
aws ce get-cost-and-usage --time-period Start=2026-07-01,End=2026-08-01 --granularity DAILY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE
```

Group by `Type=TAG,Key=team` when your org enforces cost-allocation tags.

## Find savings

```bash
aws cost-optimization-hub list-recommendations --category Compute
aws compute-optimizer get-ec2-instance-recommendations
```

Rightsize only after 14 days of steady-state utilization data; avoid churning on bursty jobs.

## Budgets and alerts

```bash
aws budgets create-budget --account-id 123456789012 --budget file://budget.json --notifications-with-subscribers file://notifications.json
```

Budget JSON example:

```json
{
  "BudgetLimit": {"Amount": "10000", "Unit": "USD"},
  "BudgetName": "monthly-engineering",
  "BudgetType": "COST",
  "TimeUnit": "MONTHLY",
  "TimePeriod": {"Start": "2026-08-01"}
}
```

## Anomaly detection

```bash
aws ce get-anomalies --monitor-arn <monitor-arn> --date-interval Start=2026-07-01
aws ce get-anomaly-monitors
```

## Best practices

- Tag everything; untagged resources are invisible to owners.
- Use Savings Plans for steady compute and Spot for interruptible work.
- Archive old S3 objects with lifecycle policies before buying more storage.
- Review the weekly cost anomaly report and close monitors with known reasons.

## Capabilities

### cost-explorer
Query AWS cost and usage data, forecasts, and reservations via the ce API.

**Parameters:**
- `time-period` (string): Start and end dates in YYYY-MM-DD format
- `granularity` (string): DAILY, MONTHLY, or HOURLY aggregation
- `metrics` (string): Metrics like UnblendedCost, BlendedCost, UsageQuantity

**Commands:**
- `aws ce get-cost-and-usage --time-period Start=2026-07-01,End=2026-08-01 --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE`
- `aws ce get-cost-forecast --time-period Start=2026-08-01,End=2026-09-01 --metric UNBLENDED_COST --granularity MONTHLY`
- `aws ce get-reservation-coverage --time-period Start=2026-07-01,End=2026-08-01`
- `aws ce get-reservation-utilization --time-period Start=2026-07-01,End=2026-08-01 --granularity DAILY`
- `aws ce get-anomalies --monitor-arn arn:aws:ce::123456789012:anomalymonitor/abc --date-interval Start=2026-07-01`

**Examples:**
- aws ce get-cost-and-usage --time-period Start=2026-07-01,End=2026-08-01 --granularity DAILY --metrics UnblendedCost --group-by Type=TAG,Key=team
- aws ce get-cost-and-usage --time-period Start=2026-07-01,End=2026-08-01 --granularity MONTHLY --metrics UnblendedCost --filter '{"Dimensions":{"Key":"SERVICE","Values":["Amazon Simple Storage Service"]}}'
- aws ce get-cost-forecast --metric UNBLENDED_COST --granularity DAILY

### optimization
Find rightsizing and cost optimization recommendations.

**Parameters:**
- `category` (string): Optimization category: Compute, Storage, License
- `account-ids` (string): AWS account id list to scan
- `implementation-effort` (string): Low, Medium, High effort filter for recommendations

**Commands:**
- `aws cost-optimization-hub list-recommendations --category Compute`
- `aws compute-optimizer get-ec2-instance-recommendations --account-ids 123456789012`
- `aws compute-optimizer get-ebs-volume-recommendations --account-ids 123456789012`
- `aws savingsplans list-savings-plans`
- `aws budgets describe-budgets --account-id 123456789012`

**Examples:**
- aws cost-optimization-hub list-recommendations --category Storage --implementation-effort High | jq '.items[] | {resourceId, estimatedSavings}'
- aws compute-optimizer get-ec2-instance-recommendations | jq '.instanceRecommendations[] | {instanceArn, finding}'
- aws budgets describe-budgets --account-id 123456789012 --budget-type COST

## References
- [AWS Cost Management Docs](https://docs.aws.amazon.com/cost-management/)
- [Compute Optimizer](https://docs.aws.amazon.com/compute-optimizer/)
- [Cost Optimization Hub](https://docs.aws.amazon.com/aws-cost-management/latest/userguide/cost-optimization-hub.html)
