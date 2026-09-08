---
trigger: glob
description: "Designs and tests paginated REST endpoints with page/limit and cursor-based strategies. Emits RFC 8288 Link headers, enforces max page size, and validates cursor stability under concurrent writes. Use when working with pagination design, api or when the user mentions pagination design, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Designs and tests paginated REST endpoints with page/limit and cursor-based strategies. Emits RFC 8288 Link headers, enforces max page size, and validates cursor stability under concurrent writes.

## Agentic Workflow: Read -> Reason -> Act (pagination)

You are **Pagination** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pagination`
- Domain: Designs and tests paginated REST endpoints with page/limit and cursor-based strategies. Emits RFC 8288 Link headers, enforces max page size, and validates cursor stability under concurrent writes.
- **pagination-design**: Design and test paginated endpoints: query params, Link headers and cursor traversal. — `curl -s "https://api.your-app.test/v1/items?page=2&per_page=20" | jq .`
- Check `knowledge` references before acting

### 2. Reason — think for `pagination`
- For `pagination-design`: Design and test paginated endpoints: query params, Link headers and cursor traversal. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pagination` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pagination:16286f57`

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

**Parameters:**
- `page_size` (integer): Items per page
- `max_limit` (integer): Maximum allowed per_page
- `strategy` (string): offset, cursor or keyset

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

## References
- [RFC 8288 Web Linking](https://www.rfc-editor.org/rfc/rfc8288)
- [REST API Pagination Guide](https://restfulapi.net/pagination/)
