---
applyTo: "**/*.json **/*.r **/*.sh"
---

# HTTPie

HTTPie CLI: expressive HTTP requests with intuitive syntax, JSON bodies, auth flags, file downloads, and streaming responses.

## Instructions

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
