---
name: "sse"
description: "Consumes and produces Server-Sent Events streams from the terminal. Streams events incrementally with curl -N, filters data lines, replays missed events via Last-Event-ID header, captures to files, and provides Python sseclient-py consumers. Use when working with sse consumption, api or when the user mentions sse consumption, api."
license: "MIT"
compatibility: "Requires pip. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(pip:*)"
---

Consumes and produces Server-Sent Events streams from the terminal. Streams events incrementally with curl -N, filters data lines, replays missed events via Last-Event-ID header, captures to files, and provides Python sseclient-py consumers.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -N http://localhost:8080/events`
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

# Server-Sent Events (SSE)

Hand-crafted skill for one-way push with Server-Sent Events.

## What this skill does

- Consumes event streams from the terminal with curl -N
- Parses data: lines and replays missed events with Last-Event-ID
- Serves push endpoints that flush events incrementally

## When to use

- One-way server push to browsers (no WebSocket needed)
- Live dashboards and activity feeds
- Simpler alternative to polling for slow-changing data

## Real commands

```bash
# Consume a stream, printing each event as it arrives
curl -N http://localhost:8080/events

# Keep only payload lines
curl -N -H 'Accept: text/event-stream' http://localhost:8080/updates | grep -E '^data:'

# Replay after a disconnect: tell the server where to resume
curl -N -H 'Last-Event-ID: 14' http://localhost:8080/events

# Capture to a file
curl -N --no-buffer http://localhost:8080/stream > events.log

# Python client
pip install sseclient-py
```

## Stream format

```
id: 15
data: {"user":42,"event":"login"}

id: 16
data: {"user":7,"event":"logout"}
```

## Python consumer

```python
import sseclient, requests

resp = requests.get("http://localhost:8080/events", stream=True)
for event in sseclient.SSEClient(resp).events():
    print(event.id, event.data)
```

## Testing

```bash
curl -N http://localhost:8080/events | head -3
curl -N --no-buffer http://localhost:8080/stream > events.log && wc -l events.log
```

## Best practices

- Send id: lines and honor Last-Event-ID on the server
- Send a comment line every 15s to keep proxies from timing out
- Set Content-Type: text/event-stream and never buffer responses

## Capabilities

### sse-consumption
Consumes and produces Server-Sent Events streams from the terminal. Streams events incrementally with curl -N, filters data lines, replays missed events via Last-Event-ID header, captures to files, and provides Python sseclient-py consumers.

**Parameters:**
- `url` (string): SSE endpoint URL
- `last_event_id` (string): Last-Event-ID header value for replay
- `accept_header` (string): Accept header (text/event-stream)

**Commands:**
- `curl -N http://localhost:8080/events`
- `curl -N -H "Accept: text/event-stream" http://localhost:8080/updates | grep -E "^data:"`
- `curl -N -H "Last-Event-ID: 14" http://localhost:8080/events`
- `curl -N --no-buffer http://localhost:8080/stream`
- `pip install sseclient-py`

**Examples:**
- curl -N http://localhost:8080/events
- curl -N -H "Accept: text/event-stream" http://localhost:8080/updates | grep -E "^data:"
- curl -N -H "Last-Event-ID: 14" http://localhost:8080/events
- curl -N --no-buffer http://localhost:8080/stream
- pip install sseclient-py

## References
- [MDN Using Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
