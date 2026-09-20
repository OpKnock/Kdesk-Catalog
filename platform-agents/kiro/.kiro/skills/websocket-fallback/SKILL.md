---
name: "websocket-fallback"
description: "Implements fallback transports when WebSockets are blocked. Negotiates Server-Sent Events, long polling, and short polling automatically, tests each transport with curl, and verifies Last-Event-ID resume for SSE. Use when working with fallback protocols, api, websocket or when the user mentions fallback protocols, api, websocket."
license: "MIT"
compatibility: "Requires curl, jq. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*)"
---

Implements fallback transports when WebSockets are blocked. Negotiates Server-Sent Events, long polling, and short polling automatically, tests each transport with curl, and verifies Last-Event-ID resume for SSE.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -N -H "Accept: text/event-stream" http://localhost:8080`
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

**Parameters:**
- `timeout` (integer): Long-poll hold time in seconds
- `transport` (string): ws, sse, longpoll, or poll
- `interval` (integer): Polling interval in seconds

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

## References
- [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Socket.IO Fallback Docs](https://socket.io/docs/v4/how-it-works/)
- [HTTP Long Polling](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest)
