---
trigger: glob
description: "Processes DynamoDB change streams: enables streams, lists shards, iterates records with shard iterators, and validates stream view types. Use when working with stream processing, api or when the user mentions stream processing, api."
globs: ["**/*.r", "**/*.sh"]
---

Processes DynamoDB change streams: enables streams, lists shards, iterates records with shard iterators, and validates stream view types.

## Agentic Workflow: Read -> Reason -> Act (dynamodb-streams)

You are **Dynamodb Streams** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `dynamodb-streams`
- Domain: Processes DynamoDB change streams: enables streams, lists shards, iterates records with shard iterators, and validates stream view types.
- **stream-processing**: Enable stream specs, list streams and shards, and read records via shard iterators. — `aws dynamodb update-table --table-name Orders --stream-specification StreamEnabl`
- Check `knowledge` and `prerequisites: aws`

### 2. Reason — think for `dynamodb-streams`
- For `stream-processing`: Enable stream specs, list streams and shards, and read records via shard iterators. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `dynamodb-streams` tools
- Tools: `Glob`, `Grep`, `Read`, `Aws` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `dynamodb-streams:61fb3970`

# DynamoDB Streams

## What this skill does

DynamoDB Streams captures item-level changes (NEW_IMAGE, OLD_IMAGE, KEYS_ONLY, NEW_AND_OLD_IMAGES) in time-ordered shards. Consumers iterate shards with shard iterators, mirroring Kinesis-style processing.

## When to use

- Feeding downstream systems (search index, analytics, cache) with table changes

- Implementing cross-table replication or audit logs

- Building change-driven workflows (send email when order status changes)

## Real commands

```bash
# Enable the stream with a view type
aws dynamodb update-table --table-name Orders --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES

# Find the stream ARN
aws dynamodbstreams list-streams --table-name Orders | jq '.Streams[0].StreamArn'

# Describe shards
aws dynamodbstreams describe-stream --stream-arn $ARN | jq '.StreamDescription.Shards'

# Get a shard iterator and read records
ITERATOR=$(aws dynamodbstreams get-shard-iterator --stream-arn $ARN --shard-id $SHARD --shard-iterator-type TRIM_HORIZON --query ShardIterator --output text)
aws dynamodbstreams get-records --shard-iterator "$ITERATOR" | jq '.Records[] | {eventName, keys: .dynamodb.Keys}'
```

## View types

- KEYS_ONLY: only partition/sort keys (cheapest)

- NEW_IMAGE: full item after the change

- OLD_IMAGE: full item before the change

- NEW_AND_OLD_IMAGES: both (most expensive)

## Testing

```bash
# Make a change and see it appear in the stream
aws dynamodb put-item --table-name Orders --item '{"orderId":{"S":"o-9"}}'
sleep 5
# re-get-records with the same iterator to see the INSERT
```

## Best practices

- Prefer `TRIM_HORIZON` for backfills, `LATEST` for live consumers.

- Shard iterators expire after 15 minutes; refresh on `ExpiredIteratorException`.

- Records are at-least-once; make consumers idempotent.

- Lambda triggers auto-manage shard iteration; for raw CLI iteration keep a checkpoint in a table.

## Capabilities

### stream-processing
Enable stream specs, list streams and shards, and read records via shard iterators.

**Parameters:**
- `table-name` (string): DynamoDB table to read streams from
- `stream-arn` (string): ARN of the table stream
- `shard-iterator-type` (string): TRIM_HORIZON, LATEST, AT_SEQUENCE_NUMBER, or AFTER_SEQUENCE_NUMBER

**Commands:**
- `aws dynamodb update-table --table-name Orders --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES`
- `aws dynamodbstreams list-streams --table-name Orders`
- `aws dynamodbstreams describe-stream --stream-arn arn:aws:dynamodb:us-east-1:123456789012:table/Orders/stream/2024-01-01T00:00:00.000`
- `aws dynamodbstreams get-shard-iterator --stream-arn arn:aws:dynamodb:us-east-1:123456789012:table/Orders/stream/2024-01-01T00:00:00.000 --shard-id shardId-0000000000 --shard-iterator-type TRIM_HORIZON`
- `aws dynamodbstreams get-records --shard-iterator "$ITERATOR"`

**Examples:**
- aws dynamodb update-table --table-name Orders --stream-specification StreamEnabled=true,StreamViewType=NEW_IMAGE
- aws dynamodbstreams list-streams --table-name Orders | jq '.Streams[0].StreamArn'
- aws dynamodbstreams get-records --shard-iterator "$(aws dynamodbstreams get-shard-iterator --stream-arn $ARN --shard-id $SHARD --shard-iterator-type TRIM_HORIZON --query ShardIterator --output text)"

## References
- [DynamoDB Streams Docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)
