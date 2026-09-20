---
applyTo: "**/*.json **/*.r **/*.sh **/*.sql"
---

Designs pagination for APIs and databases: offset vs cursor keysets, EXPLAIN verification, and link-format pagination contracts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `psql -c 'EXPLAIN ANALYZE SELECT * FROM items ORDER BY id LIM`, `curl -s 'http://localhost:8080/items?limit=100&page=3' | jq `
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

# Pagination Design

Page data without surprise performance cliffs.

## When to Use

- API list endpoints
- Admin grids and log viewers
- Any ordered data access at scale

## Offset vs cursor

- Offset (`LIMIT/OFFSET`): simple, but O(n) skip and unstable on inserts.
- Keyset/cursor (`WHERE id > x ORDER BY id LIMIT n`): stable, index-friendly.

## Verify with EXPLAIN

```bash
psql -c 'EXPLAIN ANALYZE SELECT * FROM items ORDER BY id LIMIT 50 OFFSET 50000;'
psql -c 'EXPLAIN ANALYZE SELECT * FROM items WHERE id > 50000 ORDER BY id LIMIT 50;'
```

At deep pages, keyset stays index-scan fast while offset grows linearly.

## API contract

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "abc123",
    "has_more": true
  }
}
```

Use opaque cursors (base64 of the composite key), never raw ids.

## Edge cases

- Duplicate values on the sort column: add id as tiebreaker.
- Inserts during pagination: keyset returns consistent windows.
- Huge limits: cap at 100 and return 400 beyond that.

## Best practices

- Always order by a unique key combination.
- Enforce max page size server-side.
- Return has_more/next to let clients iterate.
- Test deep pagination in load tests.

## Testing

```bash
curl -s 'https://api.example.com/items?limit=100&page=3' | jq '.items | length'
curl -s 'https://api.example.com/items?limit=-1' -o /dev/null -w '%{http_code}\n'
```

Verify page stability and input validation.

## Capabilities

### sql
Prototype and verify pagination queries in SQL.

**Parameters:**
- `db` (string): Database name
- `limit` (number): Page size
- `offset` (number): Offset value

**Commands:**
- `psql -c 'EXPLAIN ANALYZE SELECT * FROM items ORDER BY id LIMIT 50 OFFSET 50000;'`
- `psql -c 'EXPLAIN ANALYZE SELECT * FROM items WHERE id > 50000 ORDER BY id LIMIT 50;'`
- `mysql -u app -e 'SELECT COUNT(*) FROM items;'`
- `mysql -u app -e 'SELECT id, name FROM items ORDER BY id LIMIT 50 OFFSET 1000;'`
- `sqlite3 app.db "SELECT id FROM items ORDER BY id DESC LIMIT 1;"`

**Examples:**
- psql -c 'EXPLAIN ANALYZE SELECT * FROM orders WHERE created_at < %s ORDER BY created_at DESC, id DESC LIMIT 50;'
- mysql -u app -e 'EXPLAIN SELECT * FROM items WHERE id > 50000 ORDER BY id LIMIT 50;'
- sqlite3 app.db 'CREATE INDEX idx_items_id ON items(id);'

### api
Verify paginated API responses.

**Parameters:**
- `limit` (number): Page size parameter
- `cursor` (string): Opaque cursor token
- `page` (number): Offset-based page number

**Commands:**
- `curl -s 'http://localhost:8080/items?limit=100&page=3' | jq '.items | length'`
- `curl -s 'http://localhost:8080/items?limit=100&cursor=abc123' | jq '.next_page'`
- `curl -s 'http://localhost:8080/items?limit=100&page=3' | jq '{count: (.items|length), next: .links.next}'`
- `curl -s 'http://localhost:8080/items?limit=1000000' -o /dev/null -w '%{http_code}\n'`
- `curl -s 'http://localhost:8080/items?limit=50&cursor=abc' | jq '.items[0].id'`

**Examples:**
- curl -s 'http://localhost:8080/items?limit=100&page=3' | jq '.links'
- curl -s 'http://localhost:8080/items?limit=50&cursor=abc' | jq '.items | length'
- curl -s 'http://localhost:8080/items?limit=-1' -o /dev/null -w '%{http_code}\n'

## References
- [PostgreSQL LIMIT/OFFSET](https://www.postgresql.org/docs/current/queries-limit.html)
- [JSON:API pagination](https://jsonapi.org/format/#fetching-pagination)
- [Use the Index, Luke](https://use-the-index-luke.com/sql/partial-results/fetch-next-page)
