---
trigger: glob
description: "Build Kafka producers in Go with segmentio/kafka-go and IBM/sarama: async writes, batching, acks tuning, and delivery verification."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

# Kafka Producer Go

Build Kafka producers in Go with segmentio/kafka-go and IBM/sarama: async writes, batching, acks tuning, and delivery verification.

## Instructions

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

**Commands:**
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --max-messages 5`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group verify`
- `kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic orders --time -1`

**Examples:**
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning --max-messages 5
- kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic orders --time -1
