---
name: "rabbitmq-go"
description: "RabbitMQ clients in Go with amqp091-go: connection/channel management, publish/consume, and consumer recovery. Use when working with rabbitmq go client, api or when the user mentions rabbitmq go client, api."
---

RabbitMQ clients in Go with amqp091-go: connection/channel management, publish/consume, and consumer recovery.

## Agentic Workflow: Read -> Reason -> Act (rabbitmq-go)

You are **Rabbitmq Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rabbitmq-go`
- Domain: RabbitMQ clients in Go with amqp091-go: connection/channel management, publish/consume, and consumer recovery.
- **rabbitmq-go-client**: Write Go RabbitMQ publishers and consumers, manage channels and handle reconnects. — `go get github.com/rabbitmq/amqp091-go`
- Check `knowledge` and `prerequisites: rabbitmqctl`

### 2. Reason — think for `rabbitmq-go`
- For `rabbitmq-go-client`: Write Go RabbitMQ publishers and consumers, manage channels and handle reconnects. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rabbitmq-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Rabbitmqctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rabbitmq-go:efae2db1`

# RabbitMQ Go

Use amqp091-go for RabbitMQ in Go: robust connection handling and channel-based messaging.

## What this skill does

- Connects with dial config and channels
- Publishes and consumes messages
- Implements reconnection

## When to use

- Go services with RabbitMQ
- Worker queues and pub/sub

## Real commands

```bash
# Dependency
go get github.com/rabbitmq/amqp091-go
go mod tidy

# Run clients
go run publisher.go
go run consumer.go

# Inspect from CLI
rabbitmqctl list_queues name messages consumers
```

## Publisher

```go
conn, _ := amqp091.Dial("amqp://guest:guest@localhost:5672/")
ch, _ := conn.Channel()
ch.PublishWithContext(ctx, "", "tasks", false, false,
    amqp091.Publishing{ContentType: "text/plain", Body: []byte("job")})
```

## Consumer

```go
msgs, _ := ch.Consume("tasks", "", true, false, false, false, nil)
for d := range msgs {
    process(d.Body)
}
```

## Best practices

- Reconnect with backoff on connection loss
- Use prefetch (Qos) for fair dispatch
- Close channels when done; never share channels across goroutines

## Capabilities

### rabbitmq-go-client
Write Go RabbitMQ publishers and consumers, manage channels and handle reconnects.

**Parameters:**
- `queue` (string): Queue name
- `exchange` (string): Exchange name
- `url` (string): amqp:// connection URL

**Commands:**
- `go get github.com/rabbitmq/amqp091-go`
- `go mod tidy`
- `go run publisher.go`
- `go run consumer.go`
- `rabbitmqctl list_queues name messages consumers`

**Examples:**
- go run publisher.go
- rabbitmqctl list_queues name messages
- go test ./... 

## References
- [amqp091-go GitHub](https://github.com/rabbitmq/amqp091-go)
- [RabbitMQ Go guide](https://www.rabbitmq.com/clients/go-api-guide.html)
