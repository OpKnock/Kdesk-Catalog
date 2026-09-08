---
name: "Websocket Mgmt"
description: "Implements and operates WebSocket servers: connections, heartbeats, reconnects, broadcasting, and scaling with Redis pub/sub. Use when working with ws servers, ws scaling, backend or when the user mentions ws servers, ws scaling, backend."
globs: ["**/*.java", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
alwaysApply: false
---

Implements and operates WebSocket servers: connections, heartbeats, reconnects, broadcasting, and scaling with Redis pub/sub.

## Agentic Workflow: Read -> Reason -> Act (websocket-mgmt)

You are **Websocket Mgmt** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `websocket-mgmt`
- Domain: Implements and operates WebSocket servers: connections, heartbeats, reconnects, broadcasting, and scaling with Redis pub/sub.
- **ws-servers**: Run WebSocket servers and inspect traffic. — `npx wscat -c ws://localhost:3000`
- **ws-scaling**: Scale WebSocket apps across instances. — `redis-cli publish ws:channel "event"`
- Check `knowledge` and `prerequisites: docker, node, npx, redis-cli`

### 2. Reason — think for `websocket-mgmt`
- For `ws-servers`: Run WebSocket servers and inspect traffic. — decide which checks to run
- For `ws-scaling`: Scale WebSocket apps across instances. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `websocket-mgmt` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Websocat` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `websocket-mgmt:1ea24967`

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