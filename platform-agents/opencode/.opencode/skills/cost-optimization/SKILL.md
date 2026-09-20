---
name: "cost-optimization"
description: "Analyzes and reduces cloud and infrastructure costs: cost explorer queries, idle resource detection, and rightsizing. Use when working with cloud cost analysis or when the user mentions cloud cost analysis."
---

Analyzes and reduces cloud and infrastructure costs: cost explorer queries, idle resource detection, and rightsizing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aws ce get-cost-and-usage --time-period Start=$(date +%Y-%m-`
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

# Cost Optimization

Finds and eliminates cloud waste: underused compute, oversized storage, and
services running with no traffic.

## When to Use

- Monthly spend review
- Before renegotiating commitments or Reserved Instances
- Identifying orphaned resources after decommissions

## Real Commands

```bash
# Spend by service this month
aws ce get-cost-and-usage --time-period Start=$(date +%Y-%m-01) --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE

# 6-month trend
aws ce get-cost-and-usage --time-period Start=$(date -d '-6 months' +%Y-%m-01) --granularity MONTHLY --metrics UnblendedCost

# Idle instances (low CPU over 7 days)
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=i-xxxx --start-time $(date -d '-7 days' -u +%FT%TZ) --end-time $(date -u +%FT%TZ) --period 3600 --statistics Average

# Unattached elastic IPs
aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].PublicIp'

# Storage inventory
aws s3 ls --summarize --human-readable s3://bucket
```

## Container/VM waste checks

```bash
kubectl top nodes
kubectl get pods -A --field-selector=status.phase=Running | wc -l
```

## Best Practices

- Tag resources (env/cost-center) and group cost queries by tags
- Right-size instances that run < 10% CPU for weeks
- Schedule dev/staging to stop outside business hours
- Delete unattached EIPs, unused EBS snapshots, and old ECR images
- Re-evaluate RIs/SPs quarterly against actual utilization

## Example Response

Produces a spend breakdown by service, a waste list with per-item monthly cost,
and prioritized recommendations with expected savings.

## Capabilities

### cloud-cost-analysis
Query AWS cost data and find waste

**Parameters:**
- `time-period` (string): Start and End dates for the cost query
- `granularity` (string): DAILY, MONTHLY, or HOURLY cost aggregation
- `group-by` (string): Group costs by SERVICE, USAGE_TYPE, or AZ

**Commands:**
- `aws ce get-cost-and-usage --time-period Start=$(date +%Y-%m-01) --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE`
- `aws ce get-cost-and-usage --time-period Start=$(date -d '-6 months' +%Y-%m-01) --granularity MONTHLY --metrics UnblendedCost`
- `aws ec2 describe-instances --filters 'Name=instance-state-name,Values=running' --query 'Reservations[].Instances[].{id:InstanceId,type:InstanceType}'`
- `aws s3 ls --summarize s3://bucket --human-readable`
- `aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=i-xxxx --start-time $(date -d '-7 days' -u +%FT%TZ) --end-time $(date -u +%FT%TZ) --period 3600 --statistics Average`

**Examples:**
- aws ce get-cost-and-usage --time-period Start=2024-01-01 --granularity DAILY --metrics UnblendedCost | jq '.ResultsByTime[].Total.UnblendedCost.Amount'
- aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].PublicIp'
- aws cloudwatch get-metric-statistics --namespace AWS/S3 --metric-name BucketSizeBytes --dimensions Name=BucketName,Value=logs

## References
- [AWS Cost Explorer docs](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)
- [AWS Well-Architected cost pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
