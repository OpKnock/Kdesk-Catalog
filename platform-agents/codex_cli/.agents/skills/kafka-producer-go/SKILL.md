---
name: "kafka-producer-go"
description: "Build Kafka producers in Go with segmentio/kafka-go and IBM/sarama: async writes, batching, acks tuning, and delivery verification. Use when working with go producer app, delivery verify, api or when the user mentions go producer app, delivery verify, api."
license: "MIT"
compatibility: "Requires kafka-console-consumer.sh, kafka-consumer-groups.sh, kafka-run-class.sh."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(go:*) Bash(kafka-console-consumer.sh:*) Bash(kafka-consumer-groups.sh:*) Bash(kafka-run-class.sh:*)"
---

Build Kafka producers in Go with segmentio/kafka-go and IBM/sarama: async writes, batching, acks tuning, and delivery verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go get github.com/segmentio/kafka-go`, `kafka-console-consumer.sh --bootstrap-server localhost:9092 `
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
