---
trigger: glob
description: "Designs consistent REST APIs: resource modeling, status codes, versioning, pagination, filtering, and OpenAPI documentation. Use when working with rest openapi, rest testing, backend or when the user mentions rest openapi, rest testing, backend."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Designs consistent REST APIs: resource modeling, status codes, versioning, pagination, filtering, and OpenAPI documentation.

## Agentic Workflow: Read -> Reason -> Act (rest-api-design)

You are **Rest Api Design** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `rest-api-design`
- Domain: Designs consistent REST APIs: resource modeling, status codes, versioning, pagination, filtering, and OpenAPI documentation.
- **rest-openapi**: Validate and serve OpenAPI specifications. — `npx @redocly/cli lint openapi.yaml`
- **rest-testing**: Exercise endpoints and verify API behavior. — `curl -s -X POST http://localhost:8000/api/users -H "Content-Type: application/js`
- Check `knowledge` and `prerequisites: npx, python`

### 2. Reason — think for `rest-api-design`
- For `rest-openapi`: Validate and serve OpenAPI specifications. — decide which checks to run
- For `rest-testing`: Exercise endpoints and verify API behavior. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rest-api-design` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rest-api-design:4291f7e2`

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
