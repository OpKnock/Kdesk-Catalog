---
name: "websocket-mgmt"
description: "Implements and operates WebSocket servers: connections, heartbeats, reconnects, broadcasting, and scaling with Redis pub/sub. Use when working with ws servers, ws scaling, backend or when the user mentions ws servers, ws scaling, backend."
license: "MIT"
compatibility: "Requires docker, node, npx, redis-cli, websocat."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(docker:*) Bash(node:*) Bash(npx:*) Bash(redis-cli:*) Bash(websocat:*)"
---

Implements and operates WebSocket servers: connections, heartbeats, reconnects, broadcasting, and scaling with Redis pub/sub.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx wscat -c ws://localhost:3000`, `redis-cli publish ws:channel "event"`
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

# WebSocket Management

Build and operate realtime WebSocket services.

## When to Use

- Live notifications, chat, and collaborative editing
- Real-time dashboards and streaming updates
- Bidirectional protocols where polling is wasteful

## Core Concerns

- Heartbeat: ping/pong to detect dead connections
- Reconnect: exponential backoff with jitter on the client
- Broadcasting: fan out messages to rooms or all clients
- Scaling: one instance cannot hold every connection

## Commands

```bash
# Test a server
npx wscat -c ws://localhost:3000
npx wscat -c wss://example.com/socket

# With headers
npx wscat -c ws://localhost:3000 -H "Authorization: Bearer token"

# Alternative client
websocat ws://localhost:3000

# Cross-instance broadcast via Redis
redis-cli publish ws:channel '{"userId":1,"msg":"hi"}'
redis-cli pubsub numsub ws:channel
```

## Node Example

```javascript
const { WebSocketServer } = require("ws");
const wss = new WebSocketServer({ port: 3000 });

wss.on("connection", (ws) => {
  ws.isAlive = true;
  ws.on("pong", () => (ws.isAlive = true));
  ws.on("message", (data) => wss.clients.forEach((c) => c.send(data)));
});

setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);
```

## Best Practices

- Heartbeat every 20-30s and terminate silent sockets
- Limit payload size and rate per connection
- Authenticate on the upgrade request, not after connect
- Use Redis pub/sub to broadcast across instances
- Handle backpressure; do not buffer unbounded
- Load test with many concurrent connections before launch

## Capabilities

### ws-servers
Run WebSocket servers and inspect traffic.

**Parameters:**
- `url` (string): WebSocket URL
- `header` (string): Extra header

**Commands:**
- `npx wscat -c ws://localhost:3000`
- `npx wscat -c wss://localhost/socket`
- `websocat ws://localhost:3000`
- `node server.js`

**Examples:**
- npx wscat -c ws://localhost:3000 -H "Authorization: Bearer token"
- websocat -t ws://localhost:3000
- wscat -c wss://localhost --header "Origin: http://localhost:8080"

### ws-scaling
Scale WebSocket apps across instances.

**Parameters:**
- `channel` (string): Pub/sub channel
- `payload` (string): Message payload to publish

**Commands:**
- `redis-cli publish ws:channel "event"`
- `redis-cli pubsub numsub ws:channel`
- `redis-cli llen ws:connections`
- `docker compose up -d redis`

**Examples:**
- redis-cli publish notifications "{\"userId\":1,\"msg\":\"hi\"}"
- redis-cli psubscribe "ws:*"

## References
- [MDN WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Socket.IO Docs](https://socket.io/docs/)
