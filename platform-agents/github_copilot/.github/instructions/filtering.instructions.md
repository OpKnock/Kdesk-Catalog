---
applyTo: "**/*.java **/*.r **/*.sh **/*.{js,ts,jsx,tsx}"
---

# Filtering

Server-side API filtering: implement query parameter filters, combine with pagination and sorting, and test filter edge cases with jq.

## Instructions

# Filtering

## What this skill does

Filtering lets clients narrow result sets server-side instead of downloading everything. This skill covers query-parameter filters, operator conventions (eq, gte, in), combining with sort/pagination, and testing them.

## When to use

- Endpoints that return large collections
- Dashboards and reporting with many filter dimensions
- Moving client-side filtering into the API for performance

## Real commands

```bash
# Equality filter
curl -s 'http://localhost:8080/api/orders?status=paid' | jq '.data | length'

# Range operators (gte/lte) and search
curl -s 'http://localhost:8080/api/orders?total_gte=100&total_lte=500' | jq '.data[].total'
curl -s 'http://localhost:8080/api/orders?q=alice' | jq '.data | length'

# Combine with sort + pagination
curl -s 'http://localhost:8080/api/orders?status=paid&sort=-createdAt&page=2&limit=10' | jq '.meta'
```

## Implementation example

```javascript
const OPERATORS = { eq: '=', neq: '!=', gte: '>=', lte: '<=', in: 'IN' }

function buildWhere(query) {
  const clauses = []
  for (const [key, value] of Object.entries(query)) {
    const [field, op = 'eq'] = key.split('_')
    if (OPERATORS[op] && field in ORDER_FIELDS) {
      clauses.push({ field, op: OPERATORS[op], value })
    }
  }
  return clauses
}
```

## Edge cases to test

```bash
# Unknown fields are ignored
curl -s 'http://localhost:8080/api/orders?nonexistent=1' | jq '.data | length'
# Invalid operator is rejected with 400
curl -s -o /dev/null -w '%{http_code}\n' 'http://localhost:8080/api/orders?total_bogus=5'
```

## Best practices

- Whitelist filterable fields; ignore or 400 on anything else.
- Combine with sort and pagination; document the whole matrix.
- Index the filterable columns in the database.
- Use `contains` (ILIKE) sparingly; it bypasses indexes.
- Cap `in` lists to a reasonable length (e.g. 100 values).

## Capabilities

### query-filtering
Build and test filter query parameters across API data sets.

**Commands:**
- `curl -s 'http://localhost:8080/api/orders?status=paid' | jq '.data | length'`
- `curl -s 'http://localhost:8080/api/orders?status=paid&sort=-createdAt&page=2&limit=10' | jq '.meta'`
- `curl -s 'http://localhost:8080/api/orders?total_gte=100&total_lte=500' | jq '.data[].total'`
- `grep -rn 'filter' src/controllers/ | head -10`
- `curl -s 'http://localhost:8080/api/orders?q=alice' | jq '.data | length'`

**Examples:**
- curl -s 'http://localhost:8080/api/orders?status=paid&sort=-createdAt&page=2&limit=10' | jq '.meta'
- curl -s 'http://localhost:8080/api/orders?total_gte=100&total_lte=500' | jq '.data[].total'
- curl -s 'http://localhost:8080/api/orders?status=paid' | jq '.data | length'
