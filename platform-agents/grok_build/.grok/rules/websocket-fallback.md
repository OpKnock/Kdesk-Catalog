# Websocket Fallback

Implements fallback transports when WebSockets are blocked. Negotiates Server-Sent Events, long polling, and short polling automatically, tests each transport with curl, and verifies Last-Event-ID resume for SSE.

## Instructions

# WebSocket Fallback

## What this skill does

Keep realtime features working when WebSockets are blocked (proxies, firewalls, old clients) by falling back to Server-Sent Events, long polling, or short polling. Covers negotiation order and testing each transport.

## When to use

- Corporate networks block ws:// upgrade
- Building realtime features for broad client support
- Testing transport negotiation logic

## Fallback ladder

1. WebSocket (bidirectional)
2. SSE (server push only)
3. Long polling (hold connection)
4. Short polling (interval)

## Real commands

```bash
# SSE stream
curl -N -H "Accept: text/event-stream" http://localhost:8080/events

# Long polling: server holds up to 25s
curl -s --max-time 30 "http://localhost:8080/poll?timeout=25" | jq ".events"

# Immediate poll
curl -s "http://localhost:8080/poll?timeout=0" | jq ".events | length"

# Transport negotiation
curl -s -X POST http://localhost:8080/negotiate \
  -H "Content-Type: application/json" \
  -d "{\"supportsWs\":false,\"supportsSse\":true}" | jq ".transport"

# Measure SSE hold time
curl -sN http://localhost:8080/sse -H "Accept: text/event-stream" -o /dev/null -w "%{time_total}\n"
```

## SSE format

```
event: order.created
data: {"id":42}

```
`id:` lines enable Last-Event-ID resume.

## Best practices

- Negotiate transport explicitly from client capabilities
- Long polls must return immediately when events arrive
- Set conservative timeouts slightly below LB idle time
- Add `retry:` directives to SSE streams

## Testing

```bash
curl -N http://localhost:8080/events | head -3
curl -s "http://localhost:8080/poll?timeout=1" -w "\n%{time_total}s\n"
```

## Capabilities

### fallback-protocols
Implement SSE, long polling, and polling fallbacks

**Commands:**
- `curl -N -H "Accept: text/event-stream" http://localhost:8080/events`
- `curl -s --max-time 30 "http://localhost:8080/poll?timeout=25" | jq ".events"`
- `curl -s "http://localhost:8080/poll?timeout=0" | jq ".events | length"`
- `curl -s -X POST http://localhost:8080/negotiate -H "Content-Type: application/json" -d "{\"supportsWs\":false,\"supportsSse\":true}" | jq ".transport"`
- `curl -sN http://localhost:8080/sse -H "Accept: text/event-stream" -o /dev/null -w "%{time_total}"`

**Examples:**
- curl -N http://localhost:8080/events | head -5
- curl -s "http://localhost:8080/poll?timeout=25" -w "\n%{time_total}s"
- curl -s -X POST http://localhost:8080/negotiate -d "{}" | jq ".transports"