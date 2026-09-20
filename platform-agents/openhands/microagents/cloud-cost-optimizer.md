---
name: "cloud-cost-optimizer"
description: "Optimizes cloud spend with cost visibility, rightsizing, savings plans, and budget alerting on AWS, GCP, and Azure."
type: knowledge
triggers: ["cloud-cost-optimizer", "cost-visibility", "rightsizing"]
---

# cloud-cost-optimizer

Optimizes cloud spend with cost visibility, rightsizing, savings plans, and budget alerting on AWS, GCP, and Azure.

## Instructions

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
