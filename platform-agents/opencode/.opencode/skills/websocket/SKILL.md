---
name: "websocket"
description: "Build and test WebSocket endpoints: run a Node `ws` server with broadcasting and heartbeats, connect with wscat, exchange JSON and binary frames, and monitor connected clients. Use when working with ws implementation, api or when the user mentions ws implementation, api."
---

Build and test WebSocket endpoints: run a Node `ws` server with broadcasting and heartbeats, connect with wscat, exchange JSON and binary frames, and monitor connected clients.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install ws`
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

# WebSocket

## What this skill does
Build and test WebSocket endpoints: run a Node `ws` server with broadcasting and heartbeats, connect with wscat, exchange JSON and binary frames, and monitor connected clients.

## When to use
- Adding realtime push to an API
- Writing WebSocket clients
- Debugging connection drops

## Real commands
```bash
# Install and start a server
npm install ws
node server.js

# Interactive client
wscat -c ws://localhost:8080

# One-shot message
wscat -c ws://localhost:8080 -x '{"type":"ping"}'

# Connection count
curl -s http://localhost:8080/status | jq '.clients'
```

## Minimal server (server.js)
```js
const { WebSocketServer } = require('ws');
const wss = new WebSocketServer({ port: 8080, path: '/socket' });
wss.on('connection', (ws) => {
  ws.on('message', (data, isBinary) => {
    wss.clients.forEach((c) => { if (c !== ws && c.readyState === 1) c.send(data, { binary: isBinary }); });
  });
  ws.send(JSON.stringify({ type: 'welcome' }));
});
setInterval(() => {
  wss.clients.forEach((c) => { if (c.readyState === 1) c.ping(); });
}, 30000);
```

## Heartbeats
```js
ws.on('pong', () => { ws.isAlive = true; });
// Terminate connections with no pong after 2 intervals
```

## Best practices
- Terminate stale connections via ping/pong
- Use `{ binary: isBinary }` when forwarding frames
- Close code 1000 for normal, 1008 for policy violations
- Compress frames only when clients negotiate permessage-deflate

## Testing
```bash
node server.js &
wscat -c ws://localhost:8080 -x '{"type":"ping"}'
curl -s http://localhost:8080/status | jq '.clients'
```

## Capabilities

### ws-implementation
Build and test WebSocket servers and clients

**Parameters:**
- `port` (integer): Listen port for the ws server
- `path` (string): URL path the server accepts
- `protocol` (string): Subprotocol negotiation

**Commands:**
- `npm install ws`
- `node server.js`
- `wscat -c ws://localhost:8080`
- `wscat -c ws://localhost:8080 -x '{"type":"ping"}'`
- `curl -s http://localhost:8080/status | jq '.clients'`

**Examples:**
- npm install ws uws
- node server.js --port 8080 --path /socket
- wscat -c ws://localhost:8080 --wait 5

## References
- [ws on GitHub](https://github.com/websockets/ws)
- [wscat npm](https://www.npmjs.com/package/wscat)
