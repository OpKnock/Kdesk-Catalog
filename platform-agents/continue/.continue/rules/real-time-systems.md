---
name: "real-time-systems"
description: "Builds real-time features: WebSockets with wscat/websocat, SSE streams, and gRPC bidirectional streaming."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# real-time-systems

Builds real-time features: WebSockets with wscat/websocat, SSE streams, and gRPC bidirectional streaming.

## Instructions

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