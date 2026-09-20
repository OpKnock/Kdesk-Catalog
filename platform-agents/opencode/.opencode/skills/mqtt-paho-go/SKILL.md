---
name: "mqtt-paho-go"
description: "Write MQTT clients in Go with eclipse/paho.mqtt.golang: connect options, pub/sub, tokens and TLS. Use when working with paho go client, api or when the user mentions paho go client, api."
---

Write MQTT clients in Go with eclipse/paho.mqtt.golang: connect options, pub/sub, tokens and TLS.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go get github.com/eclipse/paho.mqtt.golang`
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

# Paho MQTT Go

`github.com/eclipse/paho.mqtt.golang` is the de-facto standard MQTT client for Go.

## What this skill does

- Wires the module into a Go project
- Writes publish, subscribe and request/response clients
- Handles connection loss and TLS options

## When to use

- IoT and telemetry services in Go
- Microservices that need light async messaging

## Real commands

```bash
# Add dependency
 go get github.com/eclipse/paho.mqtt.golang
go mod tidy

# Build and verify
 go run main.go
go vet ./...
go test ./...
```

## Publish client

```go
opts := mqtt.NewClientOptions().AddBroker("tcp://localhost:1883").SetClientID("go-pub")
c := mqtt.NewClient(opts)
if t := c.Connect(); t.Wait() && t.Error() != nil { log.Fatal(t.Error()) }
c.Publish("sensors/temp", 1, false, "21.5").Wait()
c.Disconnect(250)
```

## Subscribe with handler

```go
c.Subscribe("sensors/#", 0, func(_ mqtt.Client, m mqtt.Message) {
    fmt.Printf("%s: %s\n", m.Topic(), m.Payload())
})
```

## Best practices

- Always `Wait()` on tokens and check `t.Error()`
- Set `SetConnectRetry(true)` for resilient clients
- Use `ssl://` scheme + tls.Config for TLS brokers

## Capabilities

### paho-go-client
Add the Paho Go module, write connect/publish/subscribe code and run it against a broker.

**Parameters:**
- `broker` (string): Broker URL, e.g. tcp://localhost:1883 or ssl://host:8883
- `client_id` (string): Client identifier for the connection
- `topic` (string): Topic filter used in the handler

**Commands:**
- `go get github.com/eclipse/paho.mqtt.golang`
- `go mod tidy`
- `go run main.go`
- `go vet ./...`
- `go test ./...`

**Examples:**
- go get github.com/eclipse/paho.mqtt.golang@v1.5.0
- go run main.go
- go test -run TestPublish -v ./...

## References
- [Paho MQTT Go repo](https://github.com/eclipse/paho.mqtt.golang)
- [pkg.go.dev paho.mqtt.golang](https://pkg.go.dev/github.com/eclipse/paho.mqtt.golang)
