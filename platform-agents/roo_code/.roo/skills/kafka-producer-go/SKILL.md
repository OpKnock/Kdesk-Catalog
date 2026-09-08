---
name: "kafka-producer-go"
description: "Build Kafka producers in Go with segmentio/kafka-go and IBM/sarama: async writes, batching, acks tuning, and delivery verification. Use when working with go producer app, delivery verify, api or when the user mentions go producer app, delivery verify, api."
license: "MIT"
compatibility: "Requires kafka-console-consumer.sh, kafka-consumer-groups.sh, kafka-run-class.sh."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(go:*) Bash(kafka-console-consumer.sh:*) Bash(kafka-consumer-groups.sh:*) Bash(kafka-run-class.sh:*)"
---

Build Kafka producers in Go with segmentio/kafka-go and IBM/sarama: async writes, batching, acks tuning, and delivery verification.

## Agentic Workflow: Read -> Reason -> Act (kafka-producer-go)

You are **Kafka Producer Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kafka-producer-go`
- Domain: Build Kafka producers in Go with segmentio/kafka-go and IBM/sarama: async writes, batching, acks tuning, and delivery verification.
- **go-producer-app**: Scaffold and run Go producers using kafka-go Writer or sarama AsyncProducer. — `go get github.com/segmentio/kafka-go`
- **delivery-verify**: Verify produced records landed correctly with consumers and offsets. — `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --fro`
- Check `knowledge` and `prerequisites: kafka-console-consumer.sh, kafka-consumer-groups.sh, kafka-run-class.sh`

### 2. Reason — think for `kafka-producer-go`
- For `go-producer-app`: Scaffold and run Go producers using kafka-go Writer or sarama AsyncProducer. — decide which checks to run
- For `delivery-verify`: Verify produced records landed correctly with consumers and offsets. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kafka-producer-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Kafka-console-consumer.sh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kafka-producer-go:9d6f3758`

# Kafka Producer (Go)

Write high-throughput Go producers with segmentio/kafka-go or sarama.

## What this skill does

- Builds batch writers with kafka-go and async producers with sarama.
- Tunes acks, batching, and retries for throughput vs. durability.
- Verifies deliveries against the broker.

## When to use

- Go services publishing domain events.
- High-volume pipelines needing async, batched writes.
- Migrating from kafka-console-producer to app-managed producers.

## Real commands

```bash
# Dependencies
go get github.com/segmentio/kafka-go
go get github.com/IBM/sarama

# Run producer (1000 messages)
go run ./cmd/producer -topic orders -count 1000 -brokers localhost:9092

# Build
go build -o bin/producer ./cmd/producer

# Verify delivery
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic orders --from-beginning --max-messages 5
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 --topic orders --time -1
```

## Producer example (kafka-go)

```go
w := &kafka.Writer{
  Addr:         kafka.TCP("localhost:9092"),
  Topic:        "orders",
  Balancer:     &kafka.LeastBytes{},
  RequiredAcks: kafka.RequireAll,
  Async:        true,
}
for i := 0; i < 1000; i++ {
  w.WriteMessages(context.Background(), kafka.Message{
    Key:   []byte(fmt.Sprintf("order-%d", i)),
    Value: []byte(fmt.Sprintf("{"qty":%d}", i)),
  })
}
w.Close()
```

## Testing

```bash
go test ./... 
```

## Best practices

- Use Async writers for fire-and-forget at high volume; sync for critical paths.
- Set RequiredAcks to RequireAll with idempotent producers in production.
- Close the writer on shutdown so buffered messages flush.

## Capabilities

### go-producer-app
Scaffold and run Go producers using kafka-go Writer or sarama AsyncProducer.

**Parameters:**
- `topic` (string): Topic to produce to.
- `count` (integer): Number of messages to send.
- `brokers` (string): Bootstrap brokers.

**Commands:**
- `go get github.com/segmentio/kafka-go`
- `go get github.com/IBM/sarama`
- `go run ./cmd/producer -topic orders -count 1000 -brokers localhost:9092`
- `go build -o bin/producer ./cmd/producer`
- `go test ./...`

**Examples:**
- go run ./cmd/producer -topic orders -count 1000 -brokers localhost:9092
- go build -o bin/producer ./cmd/producer && ./bin/producer
- go vet ./...

### delivery-verify
Verify produced records landed correctly with consumers and offsets.

**Parameters:**
- `topic` (string): Topic to verify.

**Commands:**
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --max-messages 5`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group verify`
- `kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic orders --time -1`

**Examples:**
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --max-messages 5
- kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic orders --time -1

## References
- [segmentio/kafka-go Writer](https://pkg.go.dev/github.com/segmentio/kafka-go)
- [IBM/sarama](https://github.com/IBM/sarama)
