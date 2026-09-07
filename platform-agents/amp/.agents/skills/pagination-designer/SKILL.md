---
name: "pagination-designer"
description: "Designs and implements pagination strategies for REST and GraphQL APIs including cursor-based (keyset), offset/limit, and time-based pagination. Validates query performance with EXPLAIN, generates RFC 8288 Link headers, and optimizes for large datasets. Use when working with cursor pagination, offset pagination, graphql connections, link headers or when the user mentions cursor pagination, offset pagination, graphql connections, link headers."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*)"
---

Designs and implements pagination strategies for REST and GraphQL APIs including cursor-based (keyset), offset/limit, and time-based pagination. Validates query performance with EXPLAIN, generates RFC 8288 Link headers, and optimizes for large datasets.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl "https://api.your-app.test/users?cursor=eyJpZCI6MTAwfQ&`, `curl "https://api.your-app.test/users?offset=0&limit=20"`
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

# Pagination Designer

## What this agent does

Designs pagination for high-volume APIs: cursor-based (keyset) pagination with opaque cursors for
stability under writes, offset/limit for simple cases, Relay-style GraphQL connections, and RFC 8288
Link headers for REST. Validates query plans with EXPLAIN to ensure index usage and prevent
deep-page performance degradation.

## When to use

- Paginating large datasets (millions of rows) where offset degrades
- Building GraphQL APIs requiring Relay-compliant connections
- Implementing stable pagination for real-time data (cursor-based)
- Adding RFC 8288 Link headers for hypermedia navigation
- Optimizing slow pagination queries with proper indexing

## Real commands

```bash
# Cursor pagination (REST)
curl -s "https://api.example.com/users?limit=20" | jq ".data, .pageInfo"
curl -s "https://api.example.com/users?cursor=eyJpZCI6MTAwfQ&limit=20" | jq ".data, .pageInfo"

# Link headers
curl -sI "https://api.example.com/users?limit=20" | grep -i "^link:"

# Offset pagination
curl -s "https://api.example.com/users?offset=0&limit=20" | jq ".data, .pagination"

# GraphQL Relay connections
curl -s -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users(first: 20) { edges { node { id name } cursor } pageInfo { hasNextPage endCursor } } }"}' | jq .data
```

## REST cursor pagination response

```json
{
  "data": [...],
  "pageInfo": {
    "hasNextPage": true,
    "endCursor": "eyJpZCI6MTAwfQ",
    "hasPreviousPage": false,
    "startCursor": "eyJpZCI6ODF9"
  }
}
```

## RFC 8288 Link header

```
Link: <https://api.example.com/users?cursor=eyJpZCI6MTAwfQ&limit=20>; rel="next",
      <https://api.example.com/users?limit=20>; rel="first",
      <https://api.example.com/users?cursor=eyJpZCI6OTkwfQ&limit=20>; rel="last"
```

## GraphQL Relay connection

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

## SQL keyset pagination

```sql
-- Forward pagination (stable, uses index)
SELECT * FROM users
WHERE id > 100
ORDER BY id ASC
LIMIT 20;

-- Backward pagination
SELECT * FROM users
WHERE id < 81
ORDER BY id DESC
LIMIT 20;
```

## Testing

- Verify cursor pagination returns stable results under concurrent writes
- Test deep pagination (page 1000+) performance with EXPLAIN ANALYZE
- Validate Link header parsing with standard libraries
- Test GraphQL connections with graphql-schema-linter

## Best practices

- Prefer cursor-based for large or frequently changing datasets
- Encode cursor as base64(JSON) with sort field + tiebreaker
- Never expose database internals in cursors (use opaque tokens)
- Return totalCount only when cheap (avoid COUNT(*) on large tables)
- Use Link headers for REST; connections for GraphQL

## Capabilities

### cursor-pagination
Implements cursor-based (keyset) pagination with opaque cursors for stable, performant paging.

**Parameters:**
- `cursor_field` (string): Field to encode in cursor (e.g., id, created_at)
- `limit` (number): Page size
- `ordering` (string): Sort order (ASC, DESC)

**Commands:**
- `curl "https://api.your-app.test/users?cursor=eyJpZCI6MTAwfQ&limit=20"`
- `curl -I "https://api.your-app.test/users?cursor=eyJpZCI6MTAwfQ&limit=20" | grep -i link`

**Examples:**
- curl -s "https://api.your-app.test/users?limit=20" | jq ".data, .pageInfo"
- curl -s "https://api.your-app.test/users?cursor=eyJpZCI6MTAwfQ&limit=20" | jq ".data, .pageInfo"
- curl -sI "https://api.your-app.test/users?limit=20" | grep -i "^link:"

### offset-pagination
Implements offset/limit pagination with total count and page metadata.

**Parameters:**
- `offset` (number): Number of items to skip
- `limit` (number): Page size
- `total_count` (boolean): Include total count in response

**Commands:**
- `curl "https://api.your-app.test/users?offset=0&limit=20"`
- `curl "https://api.your-app.test/users?offset=100&limit=20"`

**Examples:**
- curl -s "https://api.your-app.test/users?offset=0&limit=20" | jq ".data, .pagination"
- curl -s "https://api.your-app.test/users?offset=100&limit=20" | jq ".data, .pagination"

### graphql-connections
Implements Relay-style cursor connections for GraphQL with edges, nodes, and pageInfo.

**Parameters:**
- `first` (number): Number of items to fetch forward
- `after` (string): Opaque cursor for forward pagination
- `last` (number): Number of items to fetch backward
- `before` (string): Opaque cursor for backward pagination

**Commands:**
- `curl -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '{"query": "{ users(first: 20) { edges { node { id name } cursor } pageInfo { hasNextPage endCursor } } }"}'`

**Examples:**
- curl -s -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '{"query": "{ users(first: 20) { edges { node { id name } cursor } pageInfo { hasNextPage endCursor } } }"}' | jq .data
- curl -s -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '{"query": "{ users(first: 20 after: \"eyJpZCI6MTAwfQ\") { edges { node { id name } cursor } pageInfo { hasNextPage endCursor } } }"}' | jq .data

### link-headers
Generates RFC 8288 Link headers for REST pagination with rel=next, prev, first, last.

**Parameters:**
- `base_url` (string): Base URL for Link header generation
- `current_cursor` (string): Current page cursor
- `limit` (number): Page size

**Commands:**
- `curl -I "https://api.your-app.test/users?limit=20" | grep -i link`

**Examples:**
- curl -sI "https://api.your-app.test/users?limit=20" | grep -i "^link:"
- curl -sI "https://api.your-app.test/users?cursor=eyJpZCI6MTAwfQ&limit=20" | grep -i "^link:"

## References
- [RFC 8288 Web Linking](https://www.rfc-editor.org/rfc/rfc8288)
- [GitHub GraphQL Pagination](https://docs.github.com/en/graphql/guides/using-pagination-in-the-graphql-api)
- [Cursor Pagination vs Offset](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#paginate-the-data)
- [Keyset Pagination](https://use-the-index-luke.com/sql/partial-results/fetch-next-page)
- [GraphQL Cursor Connections Spec](https://relay.dev/graphql/connections.htm)

## Progressive Disclosure
This skill has many capabilities. For detailed reference:
- `references/REFERENCE.md` — full capability docs and edge cases
- `scripts/` — executable helpers (see `allowed-tools`)
- `assets/` — templates and data files
Load references on demand via relative paths, not at startup.
