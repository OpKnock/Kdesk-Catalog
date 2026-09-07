---
name: "rest-api-design"
description: "Designs consistent REST APIs: resource modeling, status codes, versioning, pagination, filtering, and OpenAPI documentation. Use when working with rest openapi, rest testing, backend or when the user mentions rest openapi, rest testing, backend."
license: "MIT"
compatibility: "Requires npx, python. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(npx:*) Bash(python:*)"
---

Designs consistent REST APIs: resource modeling, status codes, versioning, pagination, filtering, and OpenAPI documentation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @redocly/cli lint openapi.yaml`, `curl -s -X POST http://localhost:8000/api/users -H "Content-`
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

# REST API Design

Design consistent, documented REST APIs.

## When to Use

- Any HTTP service that will outlive its first version
- Multi-consumer APIs where the contract matters
- Public or partner-facing integrations

## Resource Modeling

- Nouns for resources: /users, /orders/{id}
- Actions as sub-resources: /orders/{id}/cancel (POST)
- Collections support ?filter, ?sort, ?page, ?limit
- Versions in the path: /v1/users

## Status Codes

- 200 OK, 201 Created, 204 No Content
- 400 bad request, 401 unauthenticated, 403 forbidden
- 404 missing, 409 conflict, 422 validation, 429 rate limited
- 5xx only for server faults

## Commands

```bash
# Lint your OpenAPI spec
npx @redocly/cli lint openapi.yaml
npx swagger-cli validate openapi.yaml

# Bundle for distribution
npx @redocly/cli bundle openapi.yaml -o bundled.yaml

# Preview docs
npx @redocly/cli preview-docs openapi.yaml

# Exercise endpoints
curl -s -X POST http://localhost:8000/api/users -H "Content-Type: application/json" -d '{"name":"ann"}'
curl -s "http://localhost:8000/api/users?page=2&limit=20"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/users/999
```

## Best Practices

- Use consistent plural nouns and kebab-case paths
- Return error envelopes with machine-readable codes
- Paginate with page/limit and return total where cheap
- Version the API before breaking changes ship
- Document everything in OpenAPI and lint it in CI
- Use 204 for deletes, 201 with Location for creates

## Capabilities

### rest-openapi
Validate and serve OpenAPI specifications.

**Parameters:**
- `spec` (string): OpenAPI file path
- `format` (string): Spec format: yaml or json

**Commands:**
- `npx @redocly/cli lint openapi.yaml`
- `npx @redocly/cli bundle openapi.yaml -o bundled.yaml`
- `npx swagger-cli validate openapi.yaml`
- `python -m json.tool openapi.json > /dev/null`

**Examples:**
- npx @redocly/cli lint openapi.yaml --extends recommended
- npx @redocly/cli preview-docs openapi.yaml
- npx swagger-cli validate openapi.yaml

### rest-testing
Exercise endpoints and verify API behavior.

**Parameters:**
- `endpoint` (string): API endpoint URL
- `method` (string): HTTP method

**Commands:**
- `curl -s -X POST http://localhost:8000/api/users -H "Content-Type: application/json" -d "{\"name\":\"ann\"}"`
- `curl -s http://localhost:8000/api/users?page=2&limit=20`
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/users/999`
- `curl -sI http://localhost:8000/api/users`

**Examples:**
- curl -s -X DELETE -o /dev/null -w "%{http_code}" http://localhost:8000/api/users/1
- curl -s "http://localhost:8000/api/users?sort=-created_at&status=active"
- curl -s http://localhost:8000/api/users/1 | python -m json.tool

## References
- [REST API Tutorial](https://restfulapi.net)
- [OpenAPI Spec](https://spec.openapis.org/oas/v3.1.0)
- [Redocly CLI](https://redocly.com/docs/cli/)
