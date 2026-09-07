Builds real-time features: WebSockets with wscat/websocat, SSE streams, and gRPC bidirectional streaming.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `wscat -c ws://localhost:8080/ws`, `grpcurl -plaintext localhost:50051 list`
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