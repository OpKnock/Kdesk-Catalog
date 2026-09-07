---
name: "cloud-cost-optimizer"
description: "Optimizes cloud spend with cost visibility, rightsizing, savings plans, and budget alerting on AWS, GCP, and Azure. Use when working with cost visibility, rightsizing or when the user mentions cost visibility, rightsizing."
---

Optimizes cloud spend with cost visibility, rightsizing, savings plans, and budget alerting on AWS, GCP, and Azure.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aws ce get-cost-and-usage --time-period Start=2026-08-01,End`, `aws ec2 describe-instances --filters Name=instance-state-nam`
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

# Cloud Cost Optimizer

Reduce cloud spend without breaking workloads.

## When to Use

- Monthly bills creeping up without traffic growth
- Rightsizing oversized instances and idle clusters
- Setting budgets before surprises
- Evaluating savings plans vs on-demand pricing

## Method

1. Get spend breakdown by service and account
2. Find idle/oversized resources
3. Rightsize or downscale
4. Buy savings plans for steady usage
5. Set budgets and alerts for every environment

## Commands

```bash
# AWS cost explorer
aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-10 \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# Savings plan utilization
aws ce get-savings-plans-utilization --time-period Start=2026-08-01,End=2026-08-10

# GCP
gcloud billing projects describe my-project --billing-account 0X1A2B

# Azure
az cost-management query --type ActualCost \
  --scope "/subscriptions/xxx" --timeframe MonthToDate

# Rightsizing signals
kubectl top node
kubectl top pod -l app=myapp
aws ec2 describe-instances --filters Name=instance-state-name,Values=running
```

## Best Practices

- Tag resources with owner and cost-center; enforce in CI
- Downscale after hours (stop dev instances) where allowed
- Use spot/preemptible for interruptible workloads
- Review committed-use discounts quarterly as usage changes
- Set budget alerts at 50/80/100% thresholds
- Kill zombie resources: stale buckets, unused volumes, orphaned IPs

## Capabilities

### cost-visibility
Query and export cloud costs.

**Parameters:**
- `service` (string): Service to group costs by
- `period` (string): Start/End date range

**Commands:**
- `aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-10 --granularity DAILY --metrics UnblendedCost`
- `aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-10 --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE`
- `gcloud billing projects describe my-project --billing-account 0X1A2B`
- `az cost-management query --type ActualCost --scope "/subscriptions/xxx" --timeframe MonthToDate`

**Examples:**
- aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-10 --granularity DAILY --metrics UnblendedCost --group-by Type=DIMENSION,Key=USAGE_TYPE
- gcloud billing accounts list
- aws ce get-savings-plans-utilization --time-period Start=2026-08-01,End=2026-08-10

### rightsizing
Find idle and oversized resources.

**Parameters:**
- `resource` (string): Resource type to audit
- `namespace` (string): Kubernetes namespace filter

**Commands:**
- `aws ec2 describe-instances --filters Name=instance-state-name,Values=running --query "Reservations[*].Instances[*].[InstanceId,InstanceType]"`
- `kubectl top node`
- `kubectl top pod -l app=myapp`
- `docker stats --no-stream`
- `gcloud compute instances list`

**Examples:**
- kubectl get hpa -A
- aws rds describe-db-instances --query "DBInstances[*].[DBInstanceIdentifier,DBInstanceClass]"
- gcloud compute instances list --format="table(name,zone,status,machineType)"

## References
- [AWS Cost Management](https://docs.aws.amazon.com/cost-management/)
- [GCP Cost Management](https://cloud.google.com/docs/cost-management)
- [Azure Cost Optimization](https://learn.microsoft.com/azure/cost-management-billing/)
