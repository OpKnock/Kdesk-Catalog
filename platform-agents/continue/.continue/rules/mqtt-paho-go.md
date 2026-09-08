---
name: "Mqtt Paho Go"
description: "Write MQTT clients in Go with eclipse/paho.mqtt.golang: connect options, pub/sub, tokens and TLS. Use when working with paho go client, api or when the user mentions paho go client, api."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Write MQTT clients in Go with eclipse/paho.mqtt.golang: connect options, pub/sub, tokens and TLS.

## Agentic Workflow: Read -> Reason -> Act (mqtt-paho-go)

You are **Mqtt Paho Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mqtt-paho-go`
- Domain: Write MQTT clients in Go with eclipse/paho.mqtt.golang: connect options, pub/sub, tokens and TLS.
- **paho-go-client**: Add the Paho Go module, write connect/publish/subscribe code and run it against a broker. — `go get github.com/eclipse/paho.mqtt.golang`
- Check `knowledge` references before acting

### 2. Reason — think for `mqtt-paho-go`
- For `paho-go-client`: Add the Paho Go module, write connect/publish/subscribe code and run it against a broker. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mqtt-paho-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mqtt-paho-go:69594b7b`

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