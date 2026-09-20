---
name: "queue-based-architecture"
description: "Designs queue-based systems with AWS SQS and Redis Streams: queues, DLQs, consumer groups, and at-least-once semantics. Use when working with sqs, redis streams or when the user mentions sqs, redis streams."
type: knowledge
triggers: ["queue-based-architecture", "sqs", "redis-streams"]
---

Designs queue-based systems with AWS SQS and Redis Streams: queues, DLQs, consumer groups, and at-least-once semantics.

## Agentic Workflow: Read -> Reason -> Act (queue-based-architecture)

You are **queue-based-architecture** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `queue-based-architecture`
- Domain: Designs queue-based systems with AWS SQS and Redis Streams: queues, DLQs, consumer groups, and at-least-once semantics.
- **sqs**: Manage SQS queues and messages. — `aws sqs create-queue --queue-name orders --attributes VisibilityTimeout=60`
- **redis-streams**: Use Redis Streams for consumer groups and replays. — `redis-cli XADD orders:stream '*' order 42 sku A1`
- Check `knowledge` and `prerequisites: redis, rabbitmq, kafka, node.js`

### 2. Reason — think for `queue-based-architecture`
- For `sqs`: Manage SQS queues and messages. — decide which checks to run
- For `redis-streams`: Use Redis Streams for consumer groups and replays. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `queue-based-architecture` tools
- Tools: `Glob`, `Grep`, `Read`, `Aws`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `queue-based-architecture:2800cfb9`

# Queue-Based Architecture

Decouple producers and consumers with durable queues.

## When to Use

- Asynchronous processing with spikes
- Workload isolation and backpressure
- Reliable delivery with retries

## SQS basics

```bash
aws sqs create-queue --queue-name orders --attributes VisibilityTimeout=60
aws sqs send-message --queue-url $Q --message-body '{"order":42}'
aws sqs receive-message --queue-url $Q --max-number-of-messages 10
aws sqs delete-message --queue-url $Q --receipt-handle $RH
```

Receive -> process -> delete. Missing delete = reprocessing = duplicate effects.

## DLQ pattern

- Main queue: orders (maxReceiveCount=5 via redrive policy).
- DLQ: orders-dlq for poison messages.

## Redis Streams groups

```bash
redis-cli XGROUP CREATE orders:stream workers 0 MKSTREAM
redis-cli XREADGROUP GROUP workers w1 COUNT 10 BLOCK 2000 STREAMS orders:stream '>'
redis-cli XACK orders:stream workers 1723300000000-0
```

The pending-entry list tracks in-flight messages for recovery.

## At-least-once semantics

- Consumers must be idempotent.
- Use visibility timeout/claims for crash recovery.
- Track per-message processing status externally when needed.

## Best practices

- Cap batch sizes to consumer throughput.
- Alert on DLQ depth and queue age.
- Use message deduplication ids where duplicates are unacceptable.
- Test failure injection: kill consumers mid-message.

## Testing

Send 10k messages, kill a consumer, restart, and verify zero loss with counts.

## Capabilities

### sqs
Manage SQS queues and messages.

**Parameters:**
- `queue-url` (string): SQS queue URL
- `message-body` (string): Message payload
- `max-number-of-messages` (number): Batch receive size

**Commands:**
- `aws sqs create-queue --queue-name orders --attributes VisibilityTimeout=60`
- `aws sqs send-message --queue-url $QUEUE_URL --message-body '{"order":42}'`
- `aws sqs receive-message --queue-url $QUEUE_URL --max-number-of-messages 10`
- `aws sqs delete-message --queue-url $QUEUE_URL --receipt-handle $RECEIPT_HANDLE`
- `aws sqs purge-queue --queue-url $QUEUE_URL`

**Examples:**
- aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages
- aws sqs send-message --queue-url $Q --message-body file://payload.json
- aws sqs list-queues

### redis-streams
Use Redis Streams for consumer groups and replays.

**Parameters:**
- `stream` (string): Stream key
- `group` (string): Consumer group name
- `consumer` (string): Consumer name

**Commands:**
- `redis-cli XADD orders:stream '*' order 42 sku A1`
- `redis-cli XGROUP CREATE orders:stream workers 0`
- `redis-cli XREADGROUP GROUP workers w1 COUNT 10 BLOCK 2000 STREAMS orders:stream '>'`
- `redis-cli XACK orders:stream workers 1723300000000-0`
- `redis-cli XLEN orders:stream`

**Examples:**
- redis-cli XGROUP CREATE orders:stream workers 0 MKSTREAM
- redis-cli XREADGROUP GROUP workers w2 COUNT 5 STREAMS orders:stream '>'
- redis-cli XINFO GROUPS orders:stream

## References
- [Amazon SQS](https://docs.aws.amazon.com/sqs/)
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)
- [AWS Lambda + SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html)
