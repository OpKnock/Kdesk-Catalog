# Dynamodb Global Tables

Manages multi-region DynamoDB replication with Global Tables: creates replication groups, adds regions, and verifies replica status and latency.

## Instructions

# DynamoDB Global Tables

## What this skill does

Global Tables replicate DynamoDB tables across AWS regions with multi-region read/write access. Writes are propagated within seconds; the service handles conflict resolution with last-writer-wins.

## When to use

- Serving users from multiple regions with low write latency

- Building disaster recovery that survives a region failure

- Migrating an existing single-region table to multi-region

## Real commands

```bash
# Create a global table (all regions must already have an identical replica)
aws dynamodb create-global-table --global-table-name Orders --replication-group 'RegionNames=us-east-1,eu-west-1'

# Add a region to an existing global table
aws dynamodb update-global-table --global-table-name Orders --replication-group-updates '[{"Create":{"RegionName":"ap-southeast-1"}}]'

# Inspect replication status
aws dynamodb describe-global-table --global-table-name Orders | jq '.GlobalTableDescription.ReplicationGroup'

# Replication settings per region
aws dynamodb describe-global-table-settings --global-table-name Orders --region eu-west-1
```

## Prerequisites checklist

- Each region must already have the table with the same name, key schema, and point-in-time recovery.

- Both tables must have streams enabled or not, consistently.

- The replica tables must not have any pre-existing data differences for the feature to work cleanly.

## Testing

```bash
# Write in one region, read in another
aws dynamodb put-item --table-name Orders --item '{"orderId":{"S":"o-1"}}' --region us-east-1
sleep 5
aws dynamodb get-item --table-name Orders --key '{"orderId":{"S":"o-1"}}' --region eu-west-1
```

## Best practices

- Enable point-in-time recovery on every replica before creating the global table.

- Set `ReplicationStatus` monitoring via describe-global-table to catch stuck replicas.

- Use `--query` filters on large replication groups instead of parsing full JSON.

- Remember DDL (create-global-table) is free; ongoing replication costs per region for writes.

## Capabilities

### global-tables
Create and manage DynamoDB global tables and their replication regions.

**Commands:**
- `aws dynamodb create-global-table --global-table-name Orders --replication-group 'RegionNames=us-east-1,eu-west-1'`
- `aws dynamodb update-global-table --global-table-name Orders --replication-group-updates '[{"Create":{"RegionName":"ap-southeast-1"}}]'`
- `aws dynamodb describe-global-table --global-table-name Orders --region us-east-1`
- `aws dynamodb describe-global-table-settings --global-table-name Orders --region eu-west-1`
- `aws dynamodb list-global-tables`

**Examples:**
- aws dynamodb create-global-table --global-table-name Orders --replication-group 'RegionNames=us-east-1,eu-west-1'
- aws dynamodb describe-global-table --global-table-name Orders | jq '.GlobalTableDescription.ReplicationGroup'
- aws dynamodb update-global-table --global-table-name Orders --replication-group-updates '[{"Create":{"RegionName":"ap-southeast-1"}}]'