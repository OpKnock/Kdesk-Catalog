---
type: agent_requested
description: "Build Kafka consumers in Go with segmentio/kafka-go: consumer groups, manual commits, partitioning strategies, and lag verification against real brokers. Use when working with go consumer app, group ops, api or when the user mentions go consumer app, group ops, api."
---

Build Kafka consumers in Go with segmentio/kafka-go: consumer groups, manual commits, partitioning strategies, and lag verification against real brokers.

## Agentic Workflow: Read -> Reason -> Act (kafka-consumer-go)

You are **Kafka Consumer Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kafka-consumer-go`
- Domain: Build Kafka consumers in Go with segmentio/kafka-go: consumer groups, manual commits, partitioning strategies, and lag verification against real brokers.
- **go-consumer-app**: Scaffold and run a Go consumer using kafka-go Reader/ConsumerGroup APIs. — `go get github.com/segmentio/kafka-go`
- **group-ops**: Verify consumer group membership, lag, and offsets with the Kafka CLI. — `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group pa`
- Check `knowledge` and `prerequisites: kafka-console-consumer.sh, kafka-consumer-groups.sh`

### 2. Reason — think for `kafka-consumer-go`
- For `go-consumer-app`: Scaffold and run a Go consumer using kafka-go Reader/ConsumerGroup APIs. — decide which checks to run
- For `group-ops`: Verify consumer group membership, lag, and offsets with the Kafka CLI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka-consumer-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Kafka-consumer-groups.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka-consumer-go:8a50006d`

# Kafka Consumer (Go)

Write production Go consumers with segmentio/kafka-go.

## What this skill does

- Builds consumers using kafka-go Reader and ConsumerGroup.
- Handles explicit offset commits and graceful shutdown.
- Verifies group membership and lag against the broker CLI.

## When to use

- Go services consuming event streams.
- Replacing ad-hoc shell consumers with a typed app.
- Building exactly-once-ish pipelines with manual commits.

## Real commands

```bash
# Add dependency
go get github.com/segmentio/kafka-go

# Run the consumer
go run ./cmd/consumer -group payments -topic orders -brokers localhost:9092

# Build a static binary
go build -o bin/consumer ./cmd/consumer

# Verify group lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group payments

# Debug consumer from CLI
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic orders --group debug --from-beginning --max-messages 5
```

## Consumer example

```go
import (
  "context"
  "github.com/segmentio/kafka-go"
)

reader := kafka.NewReader(kafka.ReaderConfig{
  Brokers:  []string{"localhost:9092"},
  GroupID:  "payments",
  Topic:    "orders",
  MinBytes: 10e3,
  MaxBytes: 10e6,
})

for {
  m, err := reader.ReadMessage(context.Background())
  if err != nil {
    break
  }
  process(m)
  // reader.CommitMessages(ctx, m) when manual commits are enabled
}
```

## Testing

```bash
go test ./... && go vet ./...
# Produce test records
echo '{"order_id":"1"}' | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
```

## Best practices

- Always handle reader.Close() on shutdown to leave the group cleanly.
- Commit after processing, not after reading.
- Set MinBytes/MaxBytes for throughput; use FetchMaxWait to control batching.

## Capabilities

### go-consumer-app
Scaffold and run a Go consumer using kafka-go Reader/ConsumerGroup APIs.

**Parameters:**
- `group` (string): Consumer group ID.
- `topic` (string): Topic to consume.
- `brokers` (string): Comma-separated bootstrap brokers.

**Commands:**
- `go get github.com/segmentio/kafka-go`
- `go run ./cmd/consumer -group payments -topic orders -brokers localhost:9092`
- `go build -o bin/consumer ./cmd/consumer`
- `go test ./...`

**Examples:**
- go run ./cmd/consumer -group payments -topic orders -brokers localhost:9092
- go build -o bin/consumer ./cmd/consumer && ./bin/consumer
- go vet ./...

### group-ops
Verify consumer group membership, lag, and offsets with the Kafka CLI.

**Parameters:**
- `group` (string): Group ID to inspect.

**Commands:**
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments --members --verbose`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --group debug --from-beginning --max-messages 5`

**Examples:**
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments --members --verbose

## References
- [segmentio/kafka-go](https://github.com/segmentio/kafka-go)
- [kafka-go consumer docs](https://pkg.go.dev/github.com/segmentio/kafka-go)