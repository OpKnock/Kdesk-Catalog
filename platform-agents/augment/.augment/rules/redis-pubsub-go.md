---
type: agent_requested
description: "Publish and subscribe to Redis channels from Go using go-redis: channel and pattern subscriptions with graceful shutdown handling. Use when working with go redis pubsub, api or when the user mentions go redis pubsub, api."
---

Publish and subscribe to Redis channels from Go using go-redis: channel and pattern subscriptions with graceful shutdown handling.

## Agentic Workflow: Read -> Reason -> Act (redis-pubsub-go)

You are **Redis Pubsub Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `redis-pubsub-go`
- Domain: Publish and subscribe to Redis channels from Go using go-redis: channel and pattern subscriptions with graceful shutdown handling.
- **go-redis-pubsub**: Publish and subscribe to Redis channels from Go with the go-redis PubSub API — `go get github.com/redis/go-redis/v9`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `redis-pubsub-go`
- For `go-redis-pubsub`: Publish and subscribe to Redis channels from Go with the go-redis PubSub API — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-pubsub-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-pubsub-go:1cd359d1`

# Redis Pub/Sub in Go

Hand-crafted skill for Redis publish/subscribe messaging with the go-redis client.

## What this skill does

- Subscribes to exact channels and glob patterns from Go
- Publishes JSON messages from redis-cli or other producers
- Handles ReceiveMessage timeouts and reconnects in subscriber loops

## When to use

- Fanning out order events to multiple Go services
- Replacing polling with push notifications between services
- Testing channel traffic during a release

## Real commands

```bash
# Add the client
go get github.com/redis/go-redis/v9
go mod init app && go mod tidy

# Produce from the CLI while the Go subscriber runs
redis-cli -p 6379 publish events:orders '{"id":1,"total":99}'

# Inspect live channels
redis-cli -p 6379 pubsub channels
redis-cli -p 6379 pubsub numsub events:orders

# Run the subscriber
go run main.go
```

## Minimal subscriber

```go
import "github.com/redis/go-redis/v9"

sub := rdb.Subscribe(ctx, "events:orders")
defer sub.Close()

for {
    msg, err := sub.ReceiveMessage(ctx)
    if err != nil {
        log.Println("recv:", err)
        continue
    }
    log.Printf("order event: %s", msg.Payload)
}
```

## Testing

```bash
# Publish from a second terminal and watch the subscriber print
redis-cli -p 6379 publish events:orders '{"id":2,"total":49}'
redis-cli -p 6379 psubscribe 'events:*'
```

## Best practices

- Always Close() the PubSub object to avoid leaking the connection
- Run one subscriber goroutine per channel with a select on ctx.Done()
- JSON-encode payloads so every consumer can decode them safely

## Capabilities

### go-redis-pubsub
Publish and subscribe to Redis channels from Go with the go-redis PubSub API

**Parameters:**
- `channel` (string): Channel name to publish to or subscribe on
- `pattern` (string): Glob pattern like events:* used with PSubscribe
- `poolSize` (integer): go-redis connection pool size (default 10)

**Commands:**
- `go get github.com/redis/go-redis/v9`
- `go mod init app && go mod tidy`
- `go run main.go`
- `redis-cli -p 6379 publish events:orders '{"id":1,"total":99}'`
- `redis-cli -p 6379 pubsub channels`

**Examples:**
- redis-cli -p 6379 publish events:orders '{"id":1}'
- redis-cli -p 6379 pubsub channels events:*
- go run main.go

## References
- [go-redis PubSub docs](https://pkg.go.dev/github.com/redis/go-redis/v9#PubSub)
- [Redis pub/sub documentation](https://redis.io/docs/latest/develop/data-types/pubsub/)