---
trigger: glob
description: "Pulsar producers in Go: send messages, batching, delivery semantics, and performance benchmarking with pulsar-perf. Use when working with pulsar go producer, api or when the user mentions pulsar go producer, api."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

Pulsar producers in Go: send messages, batching, delivery semantics, and performance benchmarking with pulsar-perf.

## Agentic Workflow: Read -> Reason -> Act (pulsar-producer-go)

You are **Pulsar Producer Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-producer-go`
- Domain: Pulsar producers in Go: send messages, batching, delivery semantics, and performance benchmarking with pulsar-perf.
- **pulsar-go-producer**: Write Go Pulsar producers with send options and benchmark throughput with pulsar-perf. — `go run producer.go`
- Check `knowledge` and `prerequisites: bin/pulsar-client, bin/pulsar-perf`

### 2. Reason — think for `pulsar-producer-go`
- For `pulsar-go-producer`: Write Go Pulsar producers with send options and benchmark throughput with pulsar-perf. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-producer-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Bin/pulsar-client` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-producer-go:a21c0a6b`

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
