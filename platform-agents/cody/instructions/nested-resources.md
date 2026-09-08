Designs and tests REST API nested resource hierarchies with URI structures, depth limits, pagination, and RFC 8288 Link headers for client navigation.

## Agentic Workflow: Read -> Reason -> Act (nested-resources)

You are **Nested Resources** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `nested-resources`
- Domain: Designs and tests REST API nested resource hierarchies with URI structures, depth limits, pagination, and RFC 8288 Link headers for client navigation.
- **nested-resource-design**: Design and test nested REST resources: URI structure, sub-resources, and linked navigation. — `curl -s https://api.your-app.test/v1/users/42/posts`
- Check `knowledge` references before acting

### 2. Reason — think for `nested-resources`
- For `nested-resource-design`: Design and test nested REST resources: URI structure, sub-resources, and linked navigation. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nested-resources` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nested-resources:06030e4b`

# Nested Resources

Nested resources model parent-child relationships directly in the URI, e.g. /users/{id}/posts/{postId}.

## What this skill does

- Designs URI hierarchies that mirror domain relationships
- Decides when nesting is appropriate vs top-level resources
- Tests endpoints and link relations with curl

## When to use

- Designing a new REST API from scratch
- Reviewing an API where nesting is inconsistent

## Real commands

```bash
# Collection under a parent
curl -s https://api.your-app.test/v1/users/42/posts

# Deep nesting (avoid beyond 2 levels)
curl -s https://api.your-app.test/v1/users/42/posts/7/comments

# Pagination on a nested collection
curl -s 'https://api.your-app.test/v1/users/42/posts?page=2&per_page=20'

# Inspect links for navigation
curl -s https://api.your-app.test/v1/users/42/posts/7 | jq '.links'

# Create returns 201 + Location
curl -sI -X POST -H 'Content-Type: application/json' \
  -d '{"title":"t"}' https://api.your-app.test/v1/users/42/posts | grep -i location
```

## Design rules

- Nest only genuine compositions (posts belong to user)
- Never nest more than 2 levels; use query params for filters
- Reference cross-aggregates by ID (e.g. /posts/{id}/author)

## Alternative when flat

```
GET /posts?author=42
POST /posts { "user_id": 42 }
```

## Best practices

- Return `Link` headers or a `links` object for navigation
- Keep names plural and consistent across levels
- Document depth limit in the OpenAPI spec

## Capabilities

### nested-resource-design
Design and test nested REST resources: URI structure, sub-resources, and linked navigation.

**Parameters:**
- `base_url` (string): API base URL
- `parent_resource` (string): Parent resource path segment
- `depth` (integer): Maximum nesting depth allowed

**Commands:**
- `curl -s https://api.your-app.test/v1/users/42/posts`
- `curl -s https://api.your-app.test/v1/users/42/posts/7/comments`
- `curl -sI https://api.your-app.test/v1/users/42/posts`
- `curl -s https://api.your-app.test/v1/users/42/posts?page=2&per_page=20`
- `curl -s https://api.your-app.test/v1/users/42/posts/7 | jq '.links'`

**Examples:**
- curl -s https://api.your-app.test/v1/teams/3/members/5 | jq .
- curl -s 'https://api.your-app.test/v1/users/42/posts?sort=created_at.desc' | jq '.data'
- curl -sI -X POST -H 'Content-Type: application/json' -d '{"title":"t"}' https://api.your-app.test/v1/users/42/posts | grep -i location

## References
- [Microsoft REST API design](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [RESTful API Design (Fowler)](https://restfulapi.net/resource-naming/)
