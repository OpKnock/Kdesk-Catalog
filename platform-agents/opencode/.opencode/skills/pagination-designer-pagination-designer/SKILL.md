---
name: "pagination-designer-pagination-designer"
description: "Designs pagination for APIs and databases: offset vs cursor keysets, EXPLAIN verification, and link-format pagination contracts. Use when working with sql, api or when the user mentions sql, api."
---

Designs pagination for APIs and databases: offset vs cursor keysets, EXPLAIN verification, and link-format pagination contracts.

## Agentic Workflow: Read -> Reason -> Act (pagination-designer-pagination-designer)

You are **pagination-designer-pagination-designer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `pagination-designer-pagination-designer`
- Domain: Designs pagination for APIs and databases: offset vs cursor keysets, EXPLAIN verification, and link-format pagination contracts.
- **sql**: Prototype and verify pagination queries in SQL. — `psql -c 'EXPLAIN ANALYZE SELECT * FROM items ORDER BY id LIMIT 50 OFFSET 50000;'`
- **api**: Verify paginated API responses. — `curl -s 'http://localhost:8080/items?limit=100&page=3' | jq '.items | length'`
- Check `knowledge` and `prerequisites: node.js, python, postgresql, redis`

### 2. Reason — think for `pagination-designer-pagination-designer`
- For `sql`: Prototype and verify pagination queries in SQL. — decide which checks to run
- For `api`: Verify paginated API responses. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pagination-designer-pagination-designer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Mysql` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pagination-designer-pagination-designer:27b89e19`

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
