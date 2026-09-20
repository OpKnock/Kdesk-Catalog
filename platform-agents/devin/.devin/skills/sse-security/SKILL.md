---
name: "sse-security"
description: "Secures Server-Sent Events endpoints with authentication, origin validation, and reconnection safety. Requires Bearer tokens on stream connections, validates CORS headers, honors Last-Event-ID for lossless reconnects, and bounds stream duration. Use when working with sse hardening, api or when the user mentions sse hardening, api."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(timeout:*)"
---

Secures Server-Sent Events endpoints with authentication, origin validation, and reconnection safety. Requires Bearer tokens on stream connections, validates CORS headers, honors Last-Event-ID for lossless reconnects, and bounds stream duration.

## Agentic Workflow: Read -> Reason -> Act (sse-security)

You are **SSE Security** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `sse-security`
- Domain: Secures Server-Sent Events endpoints with authentication, origin validation, and reconnection safety. Requires Bearer tokens on stream connections, validates CORS headers, honors Last-Event-ID for los
- **sse-hardening**: Secures Server-Sent Events endpoints with authentication, origin validation, and reconnection safety — `curl -N -H "Authorization: Bearer $TOKEN" http://localhost:8080/events`
- Check `knowledge` references before acting

### 2. Reason — think for `sse-security`
- For `sse-hardening`: Secures Server-Sent Events endpoints with authentication, origin validation, and reconnection safety. Requires Bearer to — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sse-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Timeout` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sse-security:21f0b7bd`

# SSE Security

Hand-crafted skill for securing Server-Sent Events endpoints.

## What this skill does

- Requires auth on the event stream connection itself
- Checks CORS and Content-Type on stream responses
- Uses Last-Event-ID to resume securely after reconnects

## When to use

- Exposing event streams to browser or mobile clients
- Auditing who can open long-lived connections
- Adding reconnection safety to push notifications

## Real commands

```bash
# Unauthenticated probe: must be rejected
curl -s -o /dev/null -w '%{http_code}\n' https://events.example.com/stream

# Authenticated stream
curl -N -H "Authorization: Bearer $TOKEN" -H 'Accept: text/event-stream' https://events.example.com/stream

# Response headers: content-type + CORS
curl -sI https://events.example.com/stream | grep -iE 'content-type|access-control-allow-origin'

# Resume from an event ID after a reconnect
curl -N -H 'Last-Event-ID: 42' -H 'Accept: text/event-stream' https://events.example.com/stream

# Bound reads for probes
curl -N --max-time 30 https://events.example.com/stream | head -20
```

## Server rules

- Validate the token before opening the stream (401 otherwise)
- Set Content-Type: text/event-stream and Cache-Control: no-cache
- Emit id: lines so clients can resume with Last-Event-ID
- Never echo untrusted input into event data without escaping newlines

## Testing

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://events.example.com/stream            # expect 401
curl -N -H "Authorization: Bearer $TOKEN" https://events.example.com/stream | head -5   # expect events
```

## Best practices

- Token in a header, never in the URL (logs leak URLs)
- Set a server-side keepalive/comment every 15-30s
- Cap per-client connections and enforce re-auth on reconnect

## Capabilities

### sse-hardening
Secures Server-Sent Events endpoints with authentication, origin validation, and reconnection safety. Requires Bearer tokens on stream connections, validates CORS headers, honors Last-Event-ID for lossless reconnects, and bounds stream duration.

**Parameters:**
- `token` (string): Bearer token for SSE authentication
- `origin` (string): CORS origin header value
- `last_event_id` (string): Last-Event-ID for reconnection resume
- `max_duration` (integer): Maximum stream duration in seconds

**Commands:**
- `curl -N -H "Authorization: Bearer $TOKEN" http://localhost:8080/events`
- `curl -N -H "Origin: https://app.example.com" -H "Authorization: Bearer $TOKEN" http://localhost:8080/events`
- `curl -N -H "Last-Event-ID: 42" -H "Authorization: Bearer $TOKEN" http://localhost:8080/events`
- `timeout 30 curl -N -H "Authorization: Bearer $TOKEN" http://localhost:8080/events`

**Examples:**
- curl -N -H "Authorization: Bearer $TOKEN" http://localhost:8080/events
- curl -N -H "Origin: https://app.example.com" -H "Authorization: Bearer $TOKEN" http://localhost:8080/events
- curl -N -H "Last-Event-ID: 42" -H "Authorization: Bearer $TOKEN" http://localhost:8080/events
- timeout 30 curl -N -H "Authorization: Bearer $TOKEN" http://localhost:8080/events

## References
- [MDN Using SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
