---
name: "websocket-engineer"
description: "Build, test, and debug WebSocket servers and clients using wscat, websocat, and websocketd for real-time messaging. Use when building or debugging real-time WebSocket channels. Don't use for webhook delivery (see webhook-reliability-engineer) or one-way event streams."
license: "MIT"
compatibility: "Requires node.js, socket.io, ws, redis, nginx, kubernetes."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(websocat:*) Bash(websocketd:*) Bash(wscat:*)"
---

Build, test, and debug WebSocket servers and clients using wscat, websocat, and websocketd for real-time messaging. Use when building or debugging real-time WebSocket channels. Don't use for webhook delivery (see webhook-reliability-engineer) or one-way event streams.

## Agentic Workflow: Read -> Reason -> Act (websocket-engineer)

You are **websocket-engineer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `websocket-engineer`
- Domain: Build, test, and debug WebSocket servers and clients using wscat, websocat, and websocketd for real-time messaging. Use when building or debugging real-time WebSocket channels. Don't use for webhook d
- **Test WebSocket servers with wscat**: Connect interactively or non-interactively, send frames, and verify server responses, headers, and p — `wscat -c ws://localhost:8080`
- **Relay and stream with websocat**: Tunnel WebSocket traffic, stream files into connections, and bridge websocket endpoints for debuggin — `websocat ws://localhost:8080`
- **Run WebSocket servers with websocketd**: Turn any stdin/stdout program into a WebSocket server and serve a static demo page. — `websocketd --port=8080 ./counter.sh`
- Check `knowledge` and `prerequisites: node.js, socket.io, ws, redis`

### 2. Reason — think for `websocket-engineer`
- For `Test WebSocket servers with wscat`: Connect interactively or non-interactively, send frames, and verify server responses, headers, and protocols. — decide which checks to run
- For `Relay and stream with websocat`: Tunnel WebSocket traffic, stream files into connections, and bridge websocket endpoints for debugging. — decide which checks to run
- For `Run WebSocket servers with websocketd`: Turn any stdin/stdout program into a WebSocket server and serve a static demo page. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `websocket-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Wscat`, `Websocat` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `websocket-engineer:0c7281b0`

# WebSocket Engineering

Design and debug real-time, bidirectional, persistent connections for chat, streaming, and live data.

## When to Use

- Live chat, notifications, and collaborative editing
- Streaming market data, logs, or telemetry
- Server push where polling or SSE latency is unacceptable
- Any duplex real-time protocol you control end to end

## Handshake and Protocol

1. Client opens a GET upgrade request with Sec-WebSocket-Key; server answers 101 with Sec-WebSocket-Accept.
2. Frames are masked client-to-server and unmasked server-to-client; binary vs text must be distinguished.
3. Subprotocols negotiate application-level message formats; pick one and document it.
4. Ping/pong keepalives detect dead peers; respond to pings promptly or the stack drops you.

## Connection Lifecycle

- Clients reconnect with exponential backoff plus jitter and a max cap.
- Track a connection id per socket for correlation in logs.
- Replay missed messages: clients send a resume point (last seen sequence) on reconnect.
- Close gracefully: server sends Close frame with code 1000; clients echo and terminate.

## Scaling Patterns

- Single node: in-memory pub/sub with one socket per connection.
- Multi node: fan-out via a broker (Redis, NATS) keyed by room or user; never send from the socket owner only.
- Backpressure: slow consumers must not block the broker; use per-connection queues with drop-oldest or close policy.

## Debugging Toolkit

- wscat for quick manual tests with custom headers and subprotocols.
- websocat -t to bridge two endpoints and inspect frame flow.
- websocketd to stand up throwaway servers from shell scripts.
- Check the 101 response, Sec-WebSocket-Accept, and frame fragmentation on the wire when clients misbehave.

## Common Pitfalls

- Heartbeat only from client side; servers die silently in NAT setups.
- Broadcast loops: echoing your own messages back to the sender.
- Unbounded queue growth when a client stops reading.
- TLS mismatch (wss on plain ws port) producing confusing handshake failures.

## Production Checklist

- Ping/pong heartbeat with timeout disconnect
- Reconnect with backoff and resume semantics
- Room-level authorization at subscribe time
- Connection metrics: active count, open rate, close rate, error rate
- Graceful drain on deploy (drain connections, then stop accepting)

## Capabilities

### Test WebSocket servers with wscat
Connect interactively or non-interactively, send frames, and verify server responses, headers, and protocols.

**Parameters:**
- `headers` (string): Extra HTTP headers for the opening handshake, e.g. authorization tokens.
- `subprotocol` (string): Requested WebSocket subprotocol via -p.

**Commands:**
- `wscat -c ws://localhost:8080`
- `wscat -c wss://api.example.com/socket -H 'Authorization: Bearer demo-token'`
- `wscat -c ws://localhost:8080 --wait 5 --execute 'ping'`
- `wscat -c ws://localhost:8080 -p chat-v1`

**Examples:**
- wscat -c wss://api.example.com/socket -H 'Authorization: Bearer demo-token'
- wscat -c ws://localhost:8080 -p chat-v1

### Relay and stream with websocat
Tunnel WebSocket traffic, stream files into connections, and bridge websocket endpoints for debugging.

**Parameters:**
- `bridge` (flag): -t bridges two endpoints, forwarding frames in both directions.
- `listen port` (integer): Port for -s server mode to accept incoming connections.

**Commands:**
- `websocat ws://localhost:8080`
- `websocat -t ws://internal:8080 wss://public.example.com/socket`
- `websocat ws://localhost:8080 payload.txt`
- `websocat -s 9000`
- `websocat -b -E ws://localhost:8080`

**Examples:**
- websocat -t ws://internal:8080 wss://public.example.com/socket
- websocat -s 9000

### Run WebSocket servers with websocketd
Turn any stdin/stdout program into a WebSocket server and serve a static demo page.

**Parameters:**
- `port` (integer): Port the server listens on.
- `staticdir` (string): Directory of static files served alongside the WebSocket endpoint.

**Commands:**
- `websocketd --port=8080 ./counter.sh`
- `websocketd --port=8080 --staticdir=./public ./echo.py`
- `websocketd --port=8080 --passenv=API_KEY ./feed.sh`
- `websocketd --port=8080 --loglevel=debug ./counter.sh`

**Examples:**
- websocketd --port=8080 ./counter.sh
- websocketd --port=8080 --staticdir=./public ./echo.py

## References
- [](https://github.com/websockets/wscat)
- [](https://github.com/vi/websocat)
- [](https://github.com/joewalnes/websocketd)
- [](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
