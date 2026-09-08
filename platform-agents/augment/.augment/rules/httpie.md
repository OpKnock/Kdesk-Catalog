---
type: agent_requested
description: "HTTPie CLI: expressive HTTP requests with intuitive syntax, JSON bodies, auth flags, file downloads, and streaming responses. Use when working with httpie requests, api or when the user mentions httpie requests, api."
---

HTTPie CLI: expressive HTTP requests with intuitive syntax, JSON bodies, auth flags, file downloads, and streaming responses.

## Agentic Workflow: Read -> Reason -> Act (httpie)

You are **HTTPie** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `httpie`
- Domain: HTTPie CLI: expressive HTTP requests with intuitive syntax, JSON bodies, auth flags, file downloads, and streaming responses.
- **httpie-requests**: Compose and send HTTP requests with HTTPie's shorthand syntax. — `http http://localhost:8000/api/users`
- Check `knowledge` and `prerequisites: http`

### 2. Reason — think for `httpie`
- For `httpie-requests`: Compose and send HTTP requests with HTTPie's shorthand syntax. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `httpie` tools
- Tools: `Glob`, `Grep`, `Read`, `Http` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `httpie:6b211ae6`

# HTTPie

Human-friendly HTTP requests from the terminal.

## What this skill does

- Sends HTTP requests with intuitive `key=value` and `key:=json` syntax.
- Handles JSON bodies, file uploads, and downloads.
- Streams responses with --stream.
- Shows colorized request/response pairs by default.

## When to use

- Everyday API debugging where curl is too terse.
- Demonstrating API calls in docs or demos.
- Quick checks of headers and status codes.

## Real commands

```bash
# Simple GET
http http://localhost:8000/api/users

# POST JSON body
http POST http://localhost:8000/api/users name=John age:=30

# Explicit header
http GET http://localhost:8000/api/users/42 Accept:application/json

# Basic auth
http -a user:pass http://localhost:8000/protected

# Stream SSE-style responses
http --stream http://localhost:8000/events

# Download a file
http -d https://files.your-app.test/file.zip

# File upload
http -f POST http://localhost:8000/upload file@photo.png

# Raw JSON body
http POST http://localhost:8000/api/users <<< '{"name": "John"}'
```

## Syntax cheat sheet

- `name=John` sends a string field.
- `age:=30` sends a raw JSON value.
- `Accept:application/json` sends a header.
- `file@photo.png` attaches a file (with -f for forms).

## Testing

```bash
http -h http://localhost:8000/health  # headers only
```

## Best practices

- Use `-h`/`-b` to show only headers or only body in scripts.
- Combine with jq for assertions: `http -b ... | jq .id`.
- Use `--check-status` to fail on 4xx/5xx in CI.
- Prefer `key:=` for numbers/booleans to avoid string coercion.

## Example exchange

```
User: Create a user with JSON fields name and age.
Agent: http POST http://localhost:8000/api/users name=John age:=30
```

## Capabilities

### httpie-requests
Compose and send HTTP requests with HTTPie's shorthand syntax.

**Parameters:**
- `method` (string): HTTP method, defaults to GET.
- `url` (string): Target URL.
- `headers` (string): Header shorthand, e.g. Accept:application/json.

**Commands:**
- `http http://localhost:8000/api/users`
- `http POST http://localhost:8000/api/users name=John age:=30`
- `http -a user:pass http://localhost:8000/protected`
- `http --stream http://localhost:8000/events`
- `http -d https://files.your-app.test/file.zip`

**Examples:**
- http GET http://localhost:8000/api/users/42 Accept:application/json
- http PUT http://localhost:8000/api/users/42 name=Jane
- http -f POST http://localhost:8000/upload file@photo.png

## References
- [HTTPie Docs](https://httpie.io/docs)
- [HTTPie CLI GitHub](https://github.com/httpie/cli)