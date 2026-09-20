---
type: agent_requested
description: "Designs and tests paginated REST endpoints with page/limit and cursor-based strategies. Emits RFC 8288 Link headers, enforces max page size, and validates cursor stability under concurrent writes."
---

# Pagination

Designs and tests paginated REST endpoints with page/limit and cursor-based strategies. Emits RFC 8288 Link headers, enforces max page size, and validates cursor stability under concurrent writes.

## Instructions

# Pagination

Paginate large collections predictably so clients never have to fetch everything.

## What this skill does

- Designs page/limit and cursor APIs
- Emits RFC 8288 Link headers
- Tests pagination behavior with curl

## When to use

- New list endpoints
- Fixing slow endpoints returning unbounded data

## Real commands

```bash
# Offset pagination
curl -s "https://api.your-app.test/v1/items?page=2&per_page=20" | jq .

# Link headers
curl -sI "https://api.your-app.test/v1/items?per_page=20" | grep -i '^link:'

# Cursor pagination
curl -s "https://api.your-app.test/v1/items?cursor=eyJpZCI6MTAwfQ" | jq '.data,.next_cursor'
```

## Link header shape

```http
Link: <https://api.your-app.test/v1/items?page=2&per_page=20>; rel="next", <https://api.your-app.test/v1/items?page=1&per_page=20>; rel="prev"
```

## Response envelope

```json
{
  "data": [ ... ],
  "pagination": { "page": 2, "per_page": 20, "total": 1000 }
}
```

## Cursor vs offset

- Offset: simple, but unstable with inserts
- Cursor/keyset: stable, better for streams

## Best practices

- Cap per_page (e.g. max 100) and document it
- Include Link headers on every page
- For streams, prefer cursor pagination

## Capabilities

### pagination-design
Design and test paginated endpoints: query params, Link headers and cursor traversal.

**Commands:**
- `curl -s "https://api.your-app.test/v1/items?page=2&per_page=20" | jq .`
- `curl -sI "https://api.your-app.test/v1/items?page=1&per_page=20"`
- `curl -s "https://api.your-app.test/v1/items?cursor=eyJpZCI6MTAwfQ" | jq '.data,.next_cursor'`
- `curl -s "https://api.your-app.test/v1/items?limit=50" | jq '.links'`
- `curl -sI "https://api.your-app.test/v1/items" | grep -i '^link:'`

**Examples:**
- curl -sI "https://api.your-app.test/v1/items?per_page=20" | grep -i '^link:' | tr ',' '\n'
- curl -s "https://api.your-app.test/v1/items?page=2&per_page=20" | jq '.pagination'
- curl -s "https://api.your-app.test/v1/items?cursor=eyJpZCI6MTAwfQ" | jq '.data[0].id'