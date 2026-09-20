---
name: "nats-client-go"
description: "NATS clients in Go with nats.go: connect options, publish/subscribe, request-reply, and connection events. Use when working with nats go client, api or when the user mentions nats go client, api."
license: "MIT"
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(go:*)"
---

NATS clients in Go with nats.go: connect options, publish/subscribe, request-reply, and connection events.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go get github.com/nats-io/nats.go`
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

**Parameters:**
- `url` (string): NATS server URL, e.g. nats://localhost:4222
- `subject` (string): Subject or wildcard subscription
- `queue` (string): Queue group name for load balancing

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

## References
- [nats.go GitHub](https://github.com/nats-io/nats.go)
- [nats.go pkg docs](https://pkg.go.dev/github.com/nats-io/nats.go)
