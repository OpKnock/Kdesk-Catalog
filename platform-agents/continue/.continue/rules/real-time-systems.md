---
name: "real-time-systems"
description: "Builds real-time features: WebSockets with wscat/websocat, SSE streams, and gRPC bidirectional streaming. Use when working with websocket, grpc streams or when the user mentions websocket, grpc streams."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Builds real-time features: WebSockets with wscat/websocat, SSE streams, and gRPC bidirectional streaming.

## Agentic Workflow: Read -> Reason -> Act (real-time-systems)

You are **real-time-systems** (embedded) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — embedded context for `real-time-systems`
- Domain: Builds real-time features: WebSockets with wscat/websocat, SSE streams, and gRPC bidirectional streaming.
- **websocket**: Test and debug WebSocket endpoints. — `wscat -c ws://localhost:8080/ws`
- **grpc-streams**: Exercise streaming gRPC services. — `grpcurl -plaintext localhost:50051 list`
- Check `knowledge` and `prerequisites: c, rust, rtos, linux`

### 2. Reason — think for `real-time-systems`
- For `websocket`: Test and debug WebSocket endpoints. — decide which checks to run
- For `grpc-streams`: Exercise streaming gRPC services. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `real-time-systems` tools
- Tools: `Glob`, `Grep`, `Read`, `Wscat`, `Websocat` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `real-time-systems:0f82bb1c`

# Real-Time Systems

Build and verify live-updating systems.

## When to Use

- Chat, notifications, live dashboards
- Streaming logs and metrics
- Bidirectional sync between clients

## WebSocket testing

```bash
wscat -c ws://localhost:8080/ws
echo '{"type":"ping"}' | websocat -n ws://localhost:8080/ws
```

## SSE (server-sent events)

```bash
curl -N -H 'Accept: text/event-stream' http://localhost:8080/events
```

SSE is one-way and auto-reconnects - simpler than WebSockets for feeds.

## gRPC streams

```bash
grpcurl -plaintext -d '{"message":"hello"}' localhost:50051 chat.ChatService/Chat
```

## Architecture decisions

- WebSocket: full-duplex, persistent connections.
- SSE: server push only, HTTP-native, automatic reconnect.
- gRPC streaming: typed, efficient, for internal services.
- Protocol choice drives load balancer config (sticky vs plain HTTP).

## Reliability

- Heartbeats/pings to detect dead connections.
- Reconnect with exponential backoff and jitter.
- Buffer/ack server-side for unreliable clients.
- Scale: keep-alive connections need LB support and idle timeouts.

## Testing

```bash
wscat -c ws://localhost:8080/ws --wait 10
curl -N http://localhost:8080/events | head -5
```

Verify reconnect behavior by killing the client mid-stream.

## Capabilities

### websocket
Test and debug WebSocket endpoints.

**Parameters:**
- `url` (string): ws/wss endpoint
- `protocol` (string): Subprotocol header
- `header` (string): Extra HTTP headers

**Commands:**
- `wscat -c ws://localhost:8080/ws`
- `websocat ws://localhost:8080/ws`
- `wscat -c wss://api.example.com/ws -H 'Authorization: Bearer $TOKEN'`
- `websocat -n ws://localhost:8080/ws --protocol json`
- `curl -N http://localhost:8080/events`

**Examples:**
- wscat -c ws://localhost:8080/ws --wait 10
- echo '{"type":"ping"}' | websocat -n ws://localhost:8080/ws
- curl -N -H 'Accept: text/event-stream' http://localhost:8080/events

### grpc-streams
Exercise streaming gRPC services.

**Parameters:**
- `service` (string): Service/Method name
- `data` (string): Request JSON
- `max-msg-sz` (number): Max message size

**Commands:**
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext -d '{"message":"hello"}' localhost:50051 chat.ChatService/Chat`
- `grpcurl -plaintext -d '{"query":"tail"}' localhost:50051 logs.LogService/Stream`
- `grpcurl -plaintext -import-path proto -proto chat/chat.proto localhost:50051 chat.ChatService/Chat`
- `curl -N -G http://localhost:8080/api/events`

**Examples:**
- grpcurl -plaintext -d '{"message":"hi"}' localhost:50051 chat.ChatService/Chat | head -20
- grpcurl -plaintext -d '{}' localhost:50051 logs.LogService/Stream --max-msg-sz 10000000
- curl -N -H 'Accept: text/event-stream' http://localhost:8080/stream

## References
- [MDN WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [websocat](https://github.com/vi/websocat)
- [gRPC streaming](https://grpc.io/docs/what-is-grpc/core-concepts/)