---
type: agent_requested
description: "Pulsar producers in Go: send messages, batching, delivery semantics, and performance benchmarking with pulsar-perf. Use when working with pulsar go producer, api or when the user mentions pulsar go producer, api."
---

Pulsar producers in Go: send messages, batching, delivery semantics, and performance benchmarking with pulsar-perf.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go run producer.go`
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

# Pulsar Producer (Go)

Produce messages to Pulsar with the official Go client and benchmark throughput.

## What this skill does

- Writes Go producers with options
- Sends messages with delivery semantics
- Benchmarks with pulsar-perf

## When to use

- Ingesting events from Go services
- Capacity testing a cluster

## Real commands

```bash
# App producer
go run producer.go
go vet ./...

# CLI quick send
bin/pulsar-client produce my-topic --messages "hello"

# Benchmark
bin/pulsar-perf produce my-topic --num-producers 1 --num-messages 100000 --rate 1000
bin/pulsar-perf produce my-topic -rp 1000 --size 1024
```

## Producer code

```go
client, _ := pulsar.NewClient(pulsar.ClientOptions{URL: "pulsar://localhost:6650"})
producer, _ := client.CreateProducer(pulsar.ProducerOptions{Topic: "my-topic"})
defer producer.Close()

for i := 0; i < 100; i++ {
    producer.Send(context.Background(), &pulsar.ProducerMessage{
        Payload: []byte(fmt.Sprintf("msg-%d", i)),
    })
}
```

## Send options

- `Send` (sync) vs `SendAsync` (async)
- `DisableBlockIfQueueFull` to drop instead of block

## Best practices

- Use async sends for high throughput
- Monitor `ProducerStats` for send failures
- Size topics and partitions by benchmark results

## Capabilities

### pulsar-go-producer
Write Go Pulsar producers with send options and benchmark throughput with pulsar-perf.

**Parameters:**
- `topic` (string): Topic to produce to
- `num_messages` (integer): Messages to send in benchmark
- `rate` (integer): Target publish rate (msg/s)

**Commands:**
- `go run producer.go`
- `go vet ./...`
- `bin/pulsar-client produce my-topic --messages "hello"`
- `bin/pulsar-perf produce my-topic --num-producers 1 --num-messages 100000 --rate 1000`
- `bin/pulsar-perf produce my-topic -rp 1000 --size 1024`

**Examples:**
- go run producer.go
- bin/pulsar-perf produce my-topic --num-producers 4 --num-messages 1000000
- bin/pulsar-client produce my-topic --messages '{"id":1}' -n 3

## References
- [Pulsar Go client docs](https://pulsar.apache.org/docs/3.0.x/client-libraries-go/)
- [pulsar-perf tool](https://pulsar.apache.org/docs/3.0.x/reference-cli-tools/)