# Data Retention

Expires, archives, and rotates API data with S3 lifecycle policies, MongoDB TTL indexes, and log rotation configs for compliance and cost control.

## Instructions

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

**Commands:**
- `mongosh --quiet --eval 'db.events.createIndex({createdAt:1},{expireAfterSeconds:86400})'`
- `mongosh --quiet --eval 'db.events.getIndexes()'`
- `logrotate -d /etc/logrotate.d/api`
- `logrotate -f /etc/logrotate.d/api`

**Examples:**
- mongosh --quiet --eval 'db.events.createIndex({createdAt:1},{expireAfterSeconds:2592000})'
- mongosh --quiet --eval 'db.events.getIndexes()' | jq
- logrotate -d /etc/logrotate.d/api