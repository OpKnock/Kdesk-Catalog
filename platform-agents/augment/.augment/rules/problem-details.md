---
type: agent_requested
description: "RFC 7807 problem details: structured error responses, media types, instances, and client handling. Use when working with problem details responses, api or when the user mentions problem details responses, api."
---

RFC 7807 problem details: structured error responses, media types, instances, and client handling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -H "Accept: application/problem+json" http://localho`
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

# Problem Details

RFC 7807 standardizes machine-readable error responses with type, title, status, detail and instance.

## What this skill does

- Shapes error responses across endpoints
- Emits application/problem+json correctly
- Tests clients against structured errors

## When to use

- Consistent error handling in REST APIs
- API clients that branch on error type

## Real commands

```bash
# Verify media type and status
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" http://localhost:8080/api/orders/12345

# Inspect fields
curl -s http://localhost:8080/api/orders/12345 | jq '.title,.detail,.type'

# Validation errors
curl -s -X POST -H "Content-Type: application/json" -d '{}' http://localhost:8080/api/orders | jq .
```

## Response body

```json
{
  "type": "https://api.example.com/errors/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order with id 12345",
  "instance": "/api/orders/12345"
}
```

## Validation extension

```json
{
  "type": "https://api.example.com/errors/validation",
  "status": 400,
  "violations": [
    { "name": "amount", "reason": "must be positive" }
  ]
}
```

## Best practices

- Keep `type` stable and documented per error class
- Use 4xx status codes that match the semantics
- Log `instance` for correlation with traces

## Capabilities

### problem-details-responses
Design, emit and consume application/problem+json error payloads with extension members.

**Parameters:**
- `type` (string): Error type URI identifying the problem
- `status` (integer): HTTP status code
- `instance` (string): URI identifying the occurrence

**Commands:**
- `curl -s -H "Accept: application/problem+json" http://localhost:8080/api/orders/12345`
- `curl -s -o /dev/null -w "%{http_code} %{content_type}\n" http://localhost:8080/api/orders/12345`
- `curl -s -X POST -H "Content-Type: application/json" -d '{}' http://localhost:8080/api/orders | jq .`
- `curl -s http://localhost:8080/api/orders/12345 | jq '.title,.detail,.type'`
- `curl -sI http://localhost:8080/api/orders/12345 | grep -i content-type`

**Examples:**
- curl -s http://localhost:8080/api/orders/12345 | jq .
- curl -s -X POST -H "Content-Type: application/json" -d '{"id":"x"}' http://localhost:8080/api/orders | jq '.violations'
- curl -s -o /dev/null -w "%{content_type}\n" http://localhost:8080/api/unknown

## References
- [RFC 7807 Problem Details](https://www.rfc-editor.org/rfc/rfc7807)
- [Problem Details for HTTP APIs (rfc9457)](https://www.rfc-editor.org/rfc/rfc9457)