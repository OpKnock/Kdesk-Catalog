Patterns for consistent API error handling: structured RFC 7807 problem responses, centralized middleware to map domain exceptions to status codes, contextual logging without leaking internals, and test coverage for every error path.

## Agentic Workflow: Read -> Reason -> Act (exception-handling)

You are **Exception Handling** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `exception-handling`
- Domain: Patterns for consistent API error handling: structured RFC 7807 problem responses, centralized middleware to map domain exceptions to status codes, contextual logging without leaking internals, and te
- **error-response-design**: Define, emit, log, and test consistent error responses across API layers. — `curl -s http://localhost:8080/api/orders/999999 | jq`
- Check `knowledge` and `prerequisites: grep, node`

### 2. Reason — think for `exception-handling`
- For `error-response-design`: Define, emit, log, and test consistent error responses across API layers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `exception-handling` tools
- Tools: `Glob`, `Read`, `Bash`, `Grep` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `exception-handling:0d355b5a`

# Exception Handling

## What this skill does

Good exception handling turns crashes into structured, debuggable error responses: a consistent JSON problem format, correct status codes, contextual logs, and tested error paths.

## When to use

- Auditing an API for raw stack traces leaking to clients
- Standardizing 400/404/422/500 responses across services
- Adding error-path tests before a launch

## Real commands

```bash
# What does the API actually return on errors?
curl -s -w '\nHTTP %{http_code}\n' http://localhost:8080/api/orders/999999
curl -s http://localhost:8080/api/orders/999999 | jq

# POST with invalid body
curl -s -X POST http://localhost:8080/api/orders -H 'Content-Type: application/json' -d '{"invalid":true}' | jq '.error.code'

# Find exception classes in the codebase
 grep -rn 'NotFoundException' src/ | head -20
```

## Problem details example (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order with id 999999",
  "instance": "/api/orders/999999"
}
```

## Middleware example (Node/Express)

```javascript
app.use((err, req, res, next) => {
  const status = err.status || 500
  if (status >= 500) console.error('[unhandled]', err.stack)
  res.status(status).json({
    type: err.type || 'about:blank',
    title: err.title || err.message,
    status,
    detail: status >= 500 ? 'Internal error' : err.message
  })
})
```

## Testing error paths

```bash
# Verify a 404 shape
curl -s http://localhost:8080/api/orders/999999 | jq -e '.status == 404 and .title != null'
# Verify 500s never leak internals
curl -s -w '%{http_code}' http://localhost:8080/api/crash | grep -q 500
```

## Best practices

- Use RFC 7807 problem details; keep `type` as a documented URI.
- Log the full stack server-side, but return generic messages for 5xx.
- Never return internal exception messages to clients.
- Map domain exceptions to status codes in one place (middleware).
- Test every error path, not just the happy path.

## Capabilities

### error-response-design
Define, emit, log, and test consistent error responses across API layers.

**Parameters:**
- `endpoint` (string): API path to exercise
- `error-code` (string): Machine-readable error code like VALIDATION
- `status` (integer): HTTP status for the error class

**Commands:**
- `curl -s http://localhost:8080/api/orders/999999 | jq`
- `curl -s -w '\nHTTP %{http_code}\n' http://localhost:8080/api/orders/999999`
- `grep -rn 'NotFoundException' src/ | head -20`
- `node -e "try { throw Object.assign(new Error('boom'), {status: 422, code: 'VALIDATION'}) } catch (e) { console.log(JSON.stringify({error: e.message, code: e.code, status: e.status})) }"`
- `curl -s -X POST http://localhost:8080/api/orders -H 'Content-Type: application/json' -d '{"invalid":true}' | jq '.error.code'`

**Examples:**
- curl -s -w '\nHTTP %{http_code}\n' http://localhost:8080/api/orders/999999
- curl -s -X POST http://localhost:8080/api/orders -H 'Content-Type: application/json' -d '{"invalid":true}' | jq '.error.code'
- grep -rn 'NotFoundException' src/ | head -20

## References
- [RFC 7807 Problem Details](https://www.rfc-editor.org/rfc/rfc7807.html)