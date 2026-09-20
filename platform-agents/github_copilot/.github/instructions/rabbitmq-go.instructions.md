---
applyTo: "**/*.go **/*.r **/*.sh"
---

# Rabbitmq Go

RabbitMQ clients in Go with amqp091-go: connection/channel management, publish/consume, and consumer recovery.

## Instructions

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
