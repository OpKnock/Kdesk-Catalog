---
name: "cloud-cost-optimizer"
description: "Optimizes cloud spend with cost visibility, rightsizing, savings plans, and budget alerting on AWS, GCP, and Azure. Use when working with cost visibility, rightsizing or when the user mentions cost visibility, rightsizing."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Optimizes cloud spend with cost visibility, rightsizing, savings plans, and budget alerting on AWS, GCP, and Azure.

## Agentic Workflow: Read -> Reason -> Act (cloud-cost-optimizer)

You are **cloud-cost-optimizer** (finops) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — finops context for `cloud-cost-optimizer`
- Domain: Optimizes cloud spend with cost visibility, rightsizing, savings plans, and budget alerting on AWS, GCP, and Azure.
- **cost-visibility**: Query and export cloud costs. — `aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-10 --granul`
- **rightsizing**: Find idle and oversized resources. — `aws ec2 describe-instances --filters Name=instance-state-name,Values=running --q`
- Check `knowledge` and `prerequisites: aws-cli, gcloud, az-cli, terraform`

### 2. Reason — think for `cloud-cost-optimizer`
- For `cost-visibility`: Query and export cloud costs. — decide which checks to run
- For `rightsizing`: Find idle and oversized resources. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cloud-cost-optimizer` tools
- Tools: `Glob`, `Grep`, `Read`, `Aws`, `Gcloud` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cloud-cost-optimizer:48b9bf0f`

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