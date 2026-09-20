---
name: "Nested Resources"
description: "Designs and tests REST API nested resource hierarchies with URI structures, depth limits, pagination, and RFC 8288 Link headers for client navigation."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Nested Resources

Designs and tests REST API nested resource hierarchies with URI structures, depth limits, pagination, and RFC 8288 Link headers for client navigation.

## Instructions

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