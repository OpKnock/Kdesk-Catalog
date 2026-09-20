---
type: agent_requested
description: "Manages CloudWatch metrics and alarms: metric retrieval, alarm creation, anomaly detection, and dashboard publishing."
---

# Aws Cloudwatch

Manages CloudWatch metrics and alarms: metric retrieval, alarm creation, anomaly detection, and dashboard publishing.

## Instructions

# AWS CloudWatch

## What this skill does

Manages CloudWatch metrics and alarms: listing/querying metric namespaces, computing statistics over time windows, publishing custom metrics, and creating/test alarms.

## When to use

- Verifying an API's error rate or latency trend
- Creating an alarm for a new service
- Publishing custom application metrics

## Real commands

```bash
# Available metrics
aws cloudwatch list-metrics --namespace AWS/ApiGateway

# Query a metric over the last hour
aws cloudwatch get-metric-statistics --namespace AWS/ApiGateway --metric-name 4XXError --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 300 --statistics Sum

# Publish a custom metric
aws cloudwatch put-metric-data --namespace Custom --metric-name latency --value 120 --unit Milliseconds

# Create an alarm
aws cloudwatch put-metric-alarm --alarm-name api-5xx --metric-name 5XXError --namespace AWS/ApiGateway --statistic Sum --period 60 --evaluation-periods 3 --threshold 10 --comparison-operator GreaterThanOrEqualToThreshold

# Check alarm state
aws cloudwatch describe-alarms --state-value ALARM
```

Note: `eaws` is a typo for `aws`; always use `aws cloudwatch ...`.

## Testing

- Trigger an alarm intentionally with set-alarm-state, then reset to OK
- Verify period and evaluation-periods match your SLO window

## Best practices

- Use Sum for error counts, Average for utilization
- Attach SNS actions for actionable alerts
- Publish custom metrics with consistent units

## Capabilities

### metrics
List, query, and publish metrics.

**Commands:**
- `aws cloudwatch list-metrics --namespace AWS/ApiGateway`
- `aws cloudwatch get-metric-statistics --namespace AWS/ApiGateway --metric-name 4XXError --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 300 --statistics Sum`
- `aws cloudwatch put-metric-data --namespace Custom --metric-name latency --value 120 --unit Milliseconds`
- `aws cloudwatch list-metrics --metric-name CPUUtilization --dimensions Name=InstanceId,Value=i-12345`
- `aws cloudwatch get-metric-data --metric-data-queries file://queries.json --start-time ... --end-time ...`

**Examples:**
- aws cloudwatch get-metric-statistics --namespace AWS/ApiGateway --metric-name 5XXError --period 60 --statistics Sum --start-time $(date -u -d '1h ago' +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ)
- aws cloudwatch put-metric-data --namespace Custom --metric-name order.count --value 42 --timestamp $(date -u +%Y-%m-%dT%H:%M:%SZ)
- aws cloudwatch list-metrics --namespace AWS/Lambda --query 'Metrics[].MetricName' | sort -u

### alarms
Create and manage CloudWatch alarms.

**Commands:**
- `aws cloudwatch put-metric-alarm --alarm-name api-5xx --alarm-description "API 5xx errors" --metric-name 5XXError --namespace AWS/ApiGateway --statistic Sum --period 60 --evaluation-periods 3 --threshold 10 --comparison-operator GreaterThanOrEqualToThreshold`
- `aws cloudwatch describe-alarms --state-value ALARM`
- `aws cloudwatch describe-alarms --alarm-names api-5xx`
- `aws cloudwatch set-alarm-state --alarm-name api-5xx --state-value ALARM --state-reason "test"`
- `aws cloudwatch delete-alarms --alarm-names api-5xx`

**Examples:**
- aws cloudwatch put-metric-alarm --alarm-name api-5xx --metric-name 5XXError --namespace AWS/ApiGateway --statistic Sum --period 60 --evaluation-periods 3 --threshold 10 --comparison-operator GreaterThanOrEqualToThreshold --alarm-actions arn:aws:sns:us-east-1:123456789012:oncall
- aws cloudwatch describe-alarms --state-value ALARM --query 'MetricAlarms[].AlarmName'
- aws cloudwatch describe-alarms-for-metric --metric-name 5XXError --namespace AWS/ApiGateway