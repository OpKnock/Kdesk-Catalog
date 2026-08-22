# Redis Streams Go

Produce and consume Redis Streams from Go with go-redis: XAdd for appending, XReadGroup for consumer-group reads, XAck, and XPending introspection.

## Instructions

# Redis Streams in Go

Hand-crafted skill for Redis Streams with the go-redis client.

## What this skill does

- Adds entries to a stream with rdb.XAdd and lets Redis assign IDs
- Reads with XRead for raw tailing and XReadGroup for consumer groups
- Acknowledges processed messages and inspects pending state

## When to use

- Event sourcing with Redis Streams as the log
- Replacing polling jobs with blocking stream readers
- Implementing at-least-once processing in Go services

## Real commands

```bash
go get github.com/redis/go-redis/v9

# Seed entries from the CLI
redis-cli XADD orders * amount 99.50
redis-cli XLEN orders

# Create a group (MKSTREAM creates the stream if missing)
redis-cli XGROUP CREATE orders workers $ MKSTREAM
redis-cli XINFO GROUPS orders

# Run the Go producer/consumer
go run main.go
```

## Producer snippet

```go
id, err := rdb.XAdd(ctx, &redis.XAddArgs{
    Stream: "orders",
    Values: map[string]interface{}{"amount": 99.50, "sku": "A1"},
}).Result()
```

## Consumer snippet

```go
msgs, err := rdb.XReadGroup(ctx, &redis.XReadGroupArgs{
    Group:    "workers",
    Consumer: "c1",
    Streams:  []string{"orders", ">"},
    Count:    5,
    Block:    0,
}).Result()
for _, m := range msgs {
    for _, e := range m.Messages {
        rdb.XAck(ctx, "orders", "workers", e.ID)
    }
}
```

## Testing

```bash
redis-cli XINFO STREAM orders
redis-cli XPENDING orders workers
```

## Best practices

- Read with ">" in the Streams arg for new messages only
- Always XAck after successful handling to keep the PEL small
- Set a Block timeout so readers idle instead of busy-looping

## Capabilities

### go-redis-streams
Produce and consume Redis Streams from Go with go-redis

**Commands:**
- `go get github.com/redis/go-redis/v9`
- `redis-cli XADD orders * amount 99.50`
- `redis-cli XLEN orders`
- `redis-cli XGROUP CREATE orders workers $ MKSTREAM`
- `redis-cli XINFO GROUPS orders`

**Examples:**
- redis-cli XGROUP CREATE orders workers $ MKSTREAM
- redis-cli XINFO GROUPS orders
- go run main.go