---
name: "api-rest-specialist"
description: "Applies REST design standards: JSON:API style envelopes, problem+json errors, HATEOAS links, and idempotency handling for robust consumers. Use when working with json api style, problem errors or when the user mentions json api style, problem errors."
---

Applies REST design standards: JSON:API style envelopes, problem+json errors, HATEOAS links, and idempotency handling for robust consumers.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s http://localhost:3000/api/orders | jq '.data[0], .li`, `curl -s -X POST http://localhost:3000/api/orders -H 'Content`
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

# API REST Specialist

REST standards and conventions.

## What This Skill Does
- Applies consistent envelope and error formats
- Adds HATEOAS links and idempotency
- Makes APIs predictable for consumers

## When to Use
- Designing public APIs
- Standardizing internal service contracts
- Hardening retry behavior

## Real Commands

```bash
curl -s http://localhost:3000/api/orders | jq '.data[0], .links'
curl -s -X POST http://localhost:3000/api/orders -H 'Content-Type: application/json' -H 'Idempotency-Key: abc-123' -d '{"total":50}'
curl -s -X POST http://localhost:3000/api/orders -H 'Content-Type: application/json' -d '{}' | jq '.type, .status, .title'
```

## Problem Response

```json
{
  "type": "https://api.example.com/problems/validation",
  "title": "Validation failed",
  "status": 400,
  "detail": "total is required"
}
```

## Testing
- Repeat the same Idempotency-Key and expect the same response
- Validate error bodies match the problem format
- Check Link headers expose navigation

## Best Practices
- Document the envelope format in OpenAPI
- Store idempotency keys with TTL and status
- Keep error details machine-readable

## Capabilities

### json-api-style
Shape responses with data envelopes and links

**Parameters:**
- `idempotency-key` (string): Client-supplied retry key
- `envelope` (string): Response envelope: data/links shape
- `resource` (string): Resource collection

**Commands:**
- `curl -s http://localhost:3000/api/orders | jq '.data[0], .links'`
- `curl -s -X POST http://localhost:3000/api/orders -H 'Content-Type: application/json' -H 'Idempotency-Key: abc-123' -d '{"total":50}' | jq '.data.id'`
- `curl -s -D- -o /dev/null http://localhost:3000/api/orders | grep -i '^link:'`
- `curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:3000/api/orders -H 'Content-Type: application/json' -H 'Idempotency-Key: abc-123' -d '{"total":50}'`

**Examples:**
- Idempotency-Key deduplicates retried POSTs
- Link headers advertise related resources
- jq .data extracts the JSON:API envelope

### problem-errors
Return RFC 7807 problem details for errors

**Commands:**
- `curl -s -X POST http://localhost:3000/api/orders -H 'Content-Type: application/json' -d '{}' | jq '.type, .status, .title'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/orders/404`
- `curl -s http://localhost:3000/api/orders/404 | jq '.detail'`

**Examples:**
- -cli --help
- -api --help

## References
- [RFC 7807 Problem Details](https://www.rfc-editor.org/rfc/rfc7807)
- [JSON:API Spec](https://jsonapi.org/format/)
