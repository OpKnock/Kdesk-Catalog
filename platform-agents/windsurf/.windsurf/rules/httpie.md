---
trigger: glob
description: "HTTPie CLI: expressive HTTP requests with intuitive syntax, JSON bodies, auth flags, file downloads, and streaming responses. Use when working with httpie requests, api or when the user mentions httpie requests, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

HTTPie CLI: expressive HTTP requests with intuitive syntax, JSON bodies, auth flags, file downloads, and streaming responses.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `http http://localhost:8000/api/users`
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
