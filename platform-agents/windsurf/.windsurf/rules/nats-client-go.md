---
trigger: glob
description: "NATS clients in Go with nats.go: connect options, publish/subscribe, request-reply, and connection events."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

# Nats Client Go

NATS clients in Go with nats.go: connect options, publish/subscribe, request-reply, and connection events.

## Instructions

# NATS Go Client

nats.go is the official Go client for NATS, covering core pub/sub, JetStream and KV.

## What this skill does

- Connects to NATS with options (reconnect, credentials)
- Publishes/subscribes and does request-reply
- Uses queue groups for worker distribution

## When to use

- Go microservices with NATS messaging
- Replacing HTTP polling with NATS request-reply

## Real commands

```bash
# Dependency
 go get github.com/nats-io/nats.go
go mod tidy

# Run and verify
 go run main.go
go vet ./...
go test ./...
```

## Publish / subscribe

```go
nc, _ := nats.Connect("nats://localhost:4222")
nc.Publish("orders.created", []byte(`{"id":1}`))
sub, _ := nc.Subscribe("orders.*", func(m *nats.Msg) {
    fmt.Printf("received: %s\n", m.Data)
})
sub.Unsubscribe()
```

## Request-reply

```go
resp, err := nc.Request("service.echo", []byte("ping"), 2*time.Second)
nc.Subscribe("service.echo", func(m *nats.Msg) { m.Respond([]byte("pong")) })
```

## Queue group

```go
nc.QueueSubscribe("tasks", "workers", handler)
```

## Best practices

- Always check errors from Publish/Subscribe
- Set `nats.MaxReconnects(-1)` for resilient services
- Use request-reply timeouts matching SLA

## Capabilities

### nats-go-client
Write Go NATS clients: connect, pub/sub, request/reply with the nats.go library.

**Commands:**
- `go get github.com/nats-io/nats.go`
- `go mod tidy`
- `go run main.go`
- `go vet ./...`
- `go test ./...`

**Examples:**
- go run main.go
- go test -run TestRequestReply -v ./...
- go get github.com/nats-io/nats.go@latest
