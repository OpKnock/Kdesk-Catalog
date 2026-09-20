---
name: "api-design-engineer"
description: "Designs RESTful and GraphQL APIs with resource modeling, URL conventions, pagination, HATEOAS, and versioning."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# api-design-engineer

Designs RESTful and GraphQL APIs with resource modeling, URL conventions, pagination, HATEOAS, and versioning.

## Instructions

# API Design Engineer

Designs clean, consistent APIs: resource modeling, URLs, verbs, pagination, and versioning.

## When to Use
- Greenfield API design
- Refactoring inconsistent endpoints
- Establishing design standards

## Real Commands

```bash
# Validate the design contract
swagger-cli validate openapi.yaml
npx @stoplight/spectral-cli lint openapi.yaml

# Mock it before implementation
prism mock openapi.yaml -p 4010

# Exercise pagination
curl -s 'http://localhost:3000/api/posts?page=2&limit=10'

# Check status codes
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/posts/999999
```

## Design Rules
- Nouns not verbs: `GET /users` not `GET /getUsers`
- Plural collections, singular items
- Pagination via `page`/`limit` + `X-Total-Count`
- 2xx/3xx/4xx/5xx used honestly

## Testing
Verify every documented example against `prism mock` before backend implementation.

## Best Practices
- Version via URL prefix (`/v1`) and keep it forever
- Document error bodies in the spec
- Design first, implement second

## Capabilities

### rest-design
Model resources, verbs, status codes, and pagination for REST APIs

**Commands:**
- `curl -s 'http://localhost:3000/api/posts?page=2&limit=10' -w '\n%{http_code}'`
- `curl -s -X POST http://localhost:3000/api/posts -H 'Content-Type: application/json' -d '{"title":"Hello"}' -o /dev/null -w '%{http_code}'`
- `curl -s -X PATCH http://localhost:3000/api/posts/1 -H 'Content-Type: application/json' -d '{"title":"Updated"}' -o /dev/null -w '%{http_code}'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/api/posts/999999`
- `curl -s http://localhost:3000/api/posts -H 'Accept: application/json' | python -m json.tool`

**Examples:**
- curl -s 'http://localhost:3000/api/posts?page=2&limit=10' | python -m json.tool
- curl -s -X POST http://localhost:3000/api/posts -H 'Content-Type: application/json' -d '{"title":"Hello"}' -w 'status=%{http_code}'
- curl -s -o /dev/null -w 'not_found_status=%{http_code}\n' http://localhost:3000/api/posts/999999

### spec-authoring
Author and validate OpenAPI specs as the design contract

**Commands:**
- `swagger-cli validate openapi.yaml`
- `redocly bundle openapi.yaml -o bundled.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml`
- `openapi-generator validate -i openapi.yaml`
- `prism mock openapi.yaml -p 4010`

**Examples:**
- swagger-cli validate openapi.yaml && prism mock openapi.yaml -p 4010
- redocly bundle openapi.yaml -o bundled.yaml
- npx @stoplight/spectral-cli lint --ruleset design-rules.yaml openapi.yaml