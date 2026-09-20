---
name: "httpie-devtools"
description: "Makes human-friendly HTTP requests with httpie: intuitive syntax, pretty-printed JSON, sessions, and file uploads. Use when working with request syntax, sessions and output, devtools or when the user mentions request syntax, sessions and output, devtools."
license: "MIT"
compatibility: "Requires http."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devtools"}
allowed-tools: "Glob Grep Read Bash(http:*)"
---

Makes human-friendly HTTP requests with httpie: intuitive syntax, pretty-printed JSON, sessions, and file uploads.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `http GET http://localhost:8080/items`, `http --session user-login POST http://localhost:8080/login e`
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

# HTTPie Requests

Test and debug HTTP APIs with an ergonomic curl replacement.

## What This Skill Does

- Sends requests with `http method url` syntax
- Sets fields with `key=value` and typed `:=` syntax
- Pretty-prints JSON responses with color
- Manages cookies across requests with sessions
- Handles file uploads and form data

## When to Use

- Daily API exploration and debugging
- Writing readable test scripts for endpoints
- Teams that prefer clarity over curl flags

## Real Commands

```bash
# Basics
http GET https://api.example.com/items
http POST https://api.example.com/items name=x price:=10
http PUT https://api.example.com/items/1 name=y
http DELETE https://api.example.com/items/1

# Fields and query
http GET https://api.example.com/search q==hello      # ?q=hello
http POST https://api.example.com/items name=x price:=10 enabled:=true

# Auth and headers
http -a user:pass https://api.example.com/me
http https://api.example.com/items 'Authorization: Bearer token123'

# Sessions
http --session login POST https://api.example.com/login email=a@b.c
http --session login GET https://api.example.com/me

# Output and uploads
http --json --pretty=all GET https://api.example.com/data
http -f POST https://api.example.com/upload file@./report.pdf
http -v GET https://api.example.com/health
```

## Best Practices

- Use := for JSON types (numbers, booleans, null)
- Use sessions for multi-step auth flows
- Use --offline to draft and check request syntax without sending
- Pair with jq when piping response bodies into transformations
- Use -v or --traceback when debugging unusual responses

## Capabilities

### request-syntax
Send requests with readable syntax and inspect responses.

**Parameters:**
- `method` (string): HTTP method
- `url` (string): Request URL
- `auth` (string): user:pass basic auth via -a

**Commands:**
- `http GET http://localhost:8080/items`
- `http POST http://localhost:8080/items name=x price:=10`
- `http PUT http://localhost:8080/items/1 name=y`
- `http -a user:pass http://localhost:8080/me`
- `http http://localhost:8080/search q==hello`
- `http -v http://localhost:8080/items`

**Examples:**
- http POST http://localhost:8080/items name=x price:=10
- http http://localhost:8080/search q==hello
- http -a user:pass http://localhost:8080/me

### sessions-and-output
Reuse sessions, control output, and handle JSON/files.

**Parameters:**
- `session` (string): Session name
- `pretty` (string): Output style: all, colors, none

**Commands:**
- `http --session user-login POST http://localhost:8080/login email=a@b.c`
- `http --session user-login GET http://localhost:8080/me`
- `http --json --pretty=all GET http://localhost:8080/data`
- `http --follow -b http://localhost:8080`
- `http -f POST http://localhost:8080/upload file@./report.pdf`
- `http --offline POST http://localhost:8080/items name=x`

**Examples:**
- http --session user-login POST http://localhost:8080/login email=a@b.c
- http -f POST http://localhost:8080/upload file@./report.pdf
- http --offline POST http://localhost:8080/items name=x

## References
- [HTTPie CLI Docs](https://httpie.io/docs/cli)
- [HTTPie GitHub](https://github.com/httpie/cli)
