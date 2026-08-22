---
name: "api-pagination-engineer"
description: "Implements cursor-based (keyset) pagination for high-volume APIs: indexed SQL queries, opaque cursor encoding, next-page links, and stability under writes."
type: knowledge
triggers: ["api-pagination-engineer", "keyset-queries", "cursor-encoding"]
---

# api-pagination-engineer

Implements cursor-based (keyset) pagination for high-volume APIs: indexed SQL queries, opaque cursor encoding, next-page links, and stability under writes.

## Instructions

# API Pagination Engineer

Cursor-based pagination for scalable APIs.

## What This Skill Does
- Replaces offset pagination with index-backed keyset queries
- Encodes cursors as opaque tokens with no client math
- Returns next/prev links instead of page numbers

## When to Use
- Tables with millions of rows
- Frequently written datasets where offsets drift
- Mobile clients that need stable paging

## Real Commands

```bash
psql -d app -c "CREATE INDEX idx_users_created_id ON users(created_at, id)"
psql -d app -c "EXPLAIN ANALYZE SELECT id, name FROM users WHERE (created_at, id) > ('2024-01-01', 100) ORDER BY created_at, id LIMIT 20"
```

## Response Shape

```json
{
  "data": [...],
  "next": "https://api.example.com/users?cursor=eyJpZCI6MTIwfQ&limit=20"
}
```

## Testing
- Run EXPLAIN ANALYZE to confirm index-only scans
- Insert rows mid-pagination and verify no duplicates
- Send corrupted cursors and assert 400 with a clear message

## Best Practices
- Tie-break with an always-unique column (id) in the sort keys
- Sign cursors to prevent tampering
- Cap limit and reject negative values

## Capabilities

### keyset-queries
Build index-backed keyset queries with stable ordering

**Commands:**
- `psql -d app -c "CREATE INDEX idx_users_created_id ON users(created_at, id)"`
- `psql -d app -c "EXPLAIN ANALYZE SELECT id, name FROM users WHERE (created_at, id) > ('2024-01-01', 100) ORDER BY created_at, id LIMIT 20"`
- `curl -s 'http://localhost:3000/api/users?cursor=eyJjcmVhdGVkX2F0IjoiMjAyNC0wMS0wMSIsImlkIjoxMDB9&limit=20' | jq '.data | length'`
- `psql -d app -c "SELECT count(*) FROM users"`

**Examples:**
- psql EXPLAIN ANALYZE verifies the index is used on keyset queries
- Cursor encodes (created_at, id) as base64url for opaque page tokens
- WHERE (created_at, id) > (cursor) is stable even when rows are inserted

### cursor-encoding
Encode and decode opaque page cursors

**Commands:**
- `node -e "console.log(Buffer.from(JSON.stringify({created_at:'2024-01-01',id:100})).toString('base64url'))"`
- `node -e "console.log(JSON.parse(Buffer.from('eyJjcmVhdGVkX2F0IjoiMjAyNC0wMS0wMSIsImlkIjoxMDB9','base64url').toString()))"`
- `curl -s 'http://localhost:3000/api/users?cursor=bad%20token' -o /dev/null -w '%{http_code}\n'`
