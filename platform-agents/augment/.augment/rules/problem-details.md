---
type: agent_requested
description: "RFC 7807 problem details: structured error responses, media types, instances, and client handling. Use when working with problem details responses, api or when the user mentions problem details responses, api."
---

RFC 7807 problem details: structured error responses, media types, instances, and client handling.

## Agentic Workflow: Read -> Reason -> Act (problem-details)

You are **Problem Details** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `problem-details`
- Domain: RFC 7807 problem details: structured error responses, media types, instances, and client handling.
- **problem-details-responses**: Design, emit and consume application/problem+json error payloads with extension members. — `curl -s -H "Accept: application/problem+json" http://localhost:8080/api/orders/1`
- Check `knowledge` references before acting

### 2. Reason — think for `problem-details`
- For `problem-details-responses`: Design, emit and consume application/problem+json error payloads with extension members. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `problem-details` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `problem-details:7f9e874e`

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