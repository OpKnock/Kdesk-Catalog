---
applyTo: "**/*.json **/*.r **/*.scala **/*.sh **/*.sql"
---

Implements cursor-based (keyset) pagination for high-volume APIs: indexed SQL queries, opaque cursor encoding, next-page links, and stability under writes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `psql -d app -c "CREATE INDEX idx_users_created_id ON users(c`, `node -e "console.log(Buffer.from(JSON.stringify({created_at:`
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

**Parameters:**
- `cursor` (string): Opaque base64url token encoding the last row's sort keys
- `limit` (integer): Max rows per page, default 20
- `sort` (string): Sort columns that must match the composite index

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

**Examples:**
- -cli --help
- -api --help

## References
- [PostgreSQL Indexes Docs](https://www.postgresql.org/docs/current/indexes-intro.html)
- [Use The Index Luke - Pagination](https://use-the-index-luke.com/sql/partial-results/fetch-next-page)
