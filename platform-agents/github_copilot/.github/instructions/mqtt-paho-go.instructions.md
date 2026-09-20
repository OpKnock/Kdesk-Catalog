---
applyTo: "**/*.go **/*.r **/*.sh"
---

# Mqtt Paho Go

Write MQTT clients in Go with eclipse/paho.mqtt.golang: connect options, pub/sub, tokens and TLS.

## Instructions

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
