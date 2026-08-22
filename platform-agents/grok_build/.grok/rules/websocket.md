# WebSocket

Build and test WebSocket endpoints: run a Node `ws` server with broadcasting and heartbeats, connect with wscat, exchange JSON and binary frames, and monitor connected clients.

## Instructions

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