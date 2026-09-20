---
trigger: glob
description: "Pulsar consumers in Go: consumer creation, subscription modes, message handling and retries with pulsar-client-go. Use when working with pulsar go consumer, api or when the user mentions pulsar go consumer, api."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

Pulsar consumers in Go: consumer creation, subscription modes, message handling and retries with pulsar-client-go.

## Agentic Workflow: Read -> Reason -> Act (pulsar-consumer-go)

You are **Pulsar Consumer Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-consumer-go`
- Domain: Pulsar consumers in Go: consumer creation, subscription modes, message handling and retries with pulsar-client-go.
- **pulsar-go-consumer**: Write Go Pulsar consumers: subscribe with ack modes, receive messages and handle redelivery. — `go get github.com/apache/pulsar-client-go/pulsar`
- Check `knowledge` and `prerequisites: bin/pulsar-client`

### 2. Reason — think for `pulsar-consumer-go`
- For `pulsar-go-consumer`: Write Go Pulsar consumers: subscribe with ack modes, receive messages and handle redelivery. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-consumer-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Bin/pulsar-client` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-consumer-go:7208bc87`

# Pulsar Consumer (Go)

Consume messages from Pulsar topics with the official Go client.

## What this skill does

- Creates consumers with subscription modes
- Handles ack/negative-ack
- Processes with redelivery semantics

## When to use

- Go services consuming Pulsar events
- Worker pools over shared subscriptions

## Real commands

```bash
# Dependency
go get github.com/apache/pulsar-client-go/pulsar
go mod tidy

# Run and verify
go run consumer.go
go test ./...

# Quick consume via Pulsar CLI tools
bin/pulsar-client consume my-topic -s my-sub -n 5 --subscription-type Shared
```

## Consumer code

```go
client, _ := pulsar.NewClient(pulsar.ClientOptions{URL: "pulsar://localhost:6650"})
defer client.Close()

consumer, _ := client.Subscribe(pulsar.ConsumerOptions{
    Topic:            "my-topic",
    SubscriptionName: "worker",
    Type:             pulsar.Shared,
})
defer consumer.Close()

for i := 0; i < 10; i++ {
    msg, err := consumer.Receive(context.Background())
    if err != nil { break }
    fmt.Printf("%s: %s\n", msg.Topic(), string(msg.Payload()))
    consumer.Ack(msg)
}
```

## Best practices

- Ack or negative-ack every message
- Use Shared for parallel workers, Failover for ordered hot-standby
- Set ReceiverQueueSize appropriately per workload

## Capabilities

### pulsar-go-consumer
Write Go Pulsar consumers: subscribe with ack modes, receive messages and handle redelivery.

**Parameters:**
- `topic` (string): Topic to consume from
- `subscription` (string): Subscription name
- `sub_type` (string): Exclusive, Shared, Failover or Key_Shared

**Commands:**
- `go get github.com/apache/pulsar-client-go/pulsar`
- `go mod tidy`
- `go run consumer.go`
- `go test ./...`
- `bin/pulsar-client consume my-topic -s my-sub -n 5 --subscription-type Shared`

**Examples:**
- go run consumer.go
- bin/pulsar-client consume my-topic -s worker -n 10
- go test -run TestConsumer -v ./...

## References
- [pulsar-client-go](https://github.com/apache/pulsar-client-go)
- [Pulsar Go client docs](https://pulsar.apache.org/docs/3.0.x/client-libraries-go/)
