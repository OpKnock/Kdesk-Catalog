---
type: agent_requested
description: "Expires, archives, and rotates API data with S3 lifecycle policies, MongoDB TTL indexes, and log rotation configs for compliance and cost control. Use when working with s3 lifecycle, mongo ttl, api or when the user mentions s3 lifecycle, mongo ttl, api."
---

Expires, archives, and rotates API data with S3 lifecycle policies, MongoDB TTL indexes, and log rotation configs for compliance and cost control.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aws s3api put-bucket-lifecycle-configuration --bucket my-buc`, `mongosh --quiet --eval 'db.events.createIndex({createdAt:1},`
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

# Data Retention

Expire, archive, and rotate API data with retention policies.

## When to Use

- GDPR/CCPA compliance for stored API data
- Controlling storage costs for logs and events
- Enforcing retention windows per data class

## S3 Lifecycle

```json
{
  "Rules": [
    {
      "ID": "expire-raw-events",
      "Status": "Enabled",
      "Filter": {"Prefix": "raw/"},
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    }
  ]
}
```

```bash
aws s3api put-bucket-lifecycle-configuration --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket
```

## MongoDB TTL Index

```bash
mongosh --quiet --eval 'db.events.createIndex({createdAt:1},{expireAfterSeconds:86400})'
mongosh --quiet --eval 'db.events.getIndexes()'
```

TTL deletes documents where createdAt is older than expireAfterSeconds. Requires an indexed date field.

## Log Rotation

```
/etc/logrotate.d/api:
/var/log/api/*.log {
  daily
  rotate 30
  compress
  missingok
  notifempty
}
```

```bash
logrotate -d /etc/logrotate.d/api
logrotate -f /etc/logrotate.d/api
```

## Testing

```bash
# Verify lifecycle config is active
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket | jq '.Rules'
# Inspect TTL index options
mongosh --quiet --eval 'db.events.getIndexes()' | jq '.[] | select(.expireAfterSeconds)'
```

## Best Practices

- Define retention per data class (raw, processed, logs)
- Test TTL with small expireAfterSeconds values first
- Use transition before expiration to save costs
- Document retention in a data policy
- Monitor delete and transition metrics
- Prefer encryption and lifecycle over manual deletion

## Capabilities

### s3-lifecycle
Configure S3 bucket lifecycle policies for tiering and expiring objects

**Parameters:**
- `bucket` (string): S3 bucket name
- `days` (string): Expiration or transition days

**Commands:**
- `aws s3api put-bucket-lifecycle-configuration --bucket my-bucket --lifecycle-configuration file://lifecycle.json`
- `aws s3api get-bucket-lifecycle-configuration --bucket my-bucket`
- `aws s3api delete-bucket-lifecycle --bucket my-bucket`
- `aws s3 ls s3://my-bucket --recursive | wc -l`

**Examples:**
- aws s3api put-bucket-lifecycle-configuration --bucket my-bucket --lifecycle-configuration file://lifecycle.json
- aws s3api get-bucket-lifecycle-configuration --bucket my-bucket | jq '.Rules'
- aws s3 ls s3://my-bucket --recursive --summarize | tail -3

### mongo-ttl
Use MongoDB TTL indexes and logrotate to expire API data and logs

**Parameters:**
- `expire_seconds` (string): TTL in seconds, e.g. 86400 for one day
- `collection` (string): MongoDB collection to expire

**Commands:**
- `mongosh --quiet --eval 'db.events.createIndex({createdAt:1},{expireAfterSeconds:86400})'`
- `mongosh --quiet --eval 'db.events.getIndexes()'`
- `logrotate -d /etc/logrotate.d/api`
- `logrotate -f /etc/logrotate.d/api`

**Examples:**
- mongosh --quiet --eval 'db.events.createIndex({createdAt:1},{expireAfterSeconds:2592000})'
- mongosh --quiet --eval 'db.events.getIndexes()' | jq
- logrotate -d /etc/logrotate.d/api

## References
- [S3 Lifecycle Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [MongoDB TTL Indexes](https://www.mongodb.com/docs/manual/core/index-ttl/)