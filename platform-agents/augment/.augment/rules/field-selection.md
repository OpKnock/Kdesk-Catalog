---
type: agent_requested
description: "API field selection: allow clients to request only the fields they need (sparse fieldsets), reduce payload size, and validate selections with jq and GraphQL-style patterns."
---

# Field Selection

API field selection: allow clients to request only the fields they need (sparse fieldsets), reduce payload size, and validate selections with jq and GraphQL-style patterns.

## Instructions

# Field Selection

## What this skill does

Field selection lets clients fetch only the fields they use, shrinking payloads and server work. The JSON:API convention uses `?fields=type=field1,field2`; simpler APIs use `?fields=a,b,c`. This skill implements and validates that pattern.

## When to use

- Mobile clients that need small payloads
- APIs whose default responses are bloated
- Enforcing an allowlist so clients can't request arbitrary fields

## Real commands

```bash
# Request only the fields you need
curl -s 'http://localhost:8080/api/orders/1?fields=id,status,total' | jq 'keys'

# Measure payload savings
curl -s 'http://localhost:8080/api/orders/1' | jq '. | length'          # full
curl -s 'http://localhost:8080/api/orders/1?fields=id,status' | jq '. | length'  # sparse

# Find existing selection handling
 grep -rn 'req.query.fields' src/ | head -10
```

## Implementation example (Express)

```javascript
const SELECTABLE = new Set(['id', 'status', 'total', 'createdAt'])

app.get('/api/orders/:id', (req, res) => {
  const wanted = (req.query.fields || '').split(',').filter(f => SELECTABLE.has(f))
  const order = db.get(req.params.id)
  res.json(pick(order, wanted.length ? wanted : Object.keys(SELECTABLE)))
})
```

## Validation

```bash
# Unknown fields must be rejected or ignored, never echoed
curl -s 'http://localhost:8080/api/orders/1?fields=id,__proto__,total' | jq 'keys'
```

## Best practices

- Always apply an allowlist; never build objects from raw input keys.
- Default to a sane subset when `fields` is absent.
- Document every selectable field in the OpenAPI spec.
- For deeply nested resources, consider GraphQL or JSON:API includes syntax.
- Measure payload size before/after and set budgets per endpoint.

## Capabilities

### sparse-fieldsets
Implement and test field selection parameters like ?fields= and verify payload savings.

**Commands:**
- `curl -s 'http://localhost:8080/api/orders/1?fields=id,status,total' | jq 'keys'`
- `curl -s 'http://localhost:8080/api/orders/1?fields=id,status,total' | jq 'length'`
- `curl -s 'http://localhost:8080/api/orders/1' | jq '. | length'`
- `grep -rn 'req.query.fields' src/ | head -10`
- `curl -s 'http://localhost:8080/api/orders?fields=id&page=1&limit=5' | jq '.data[0]'`

**Examples:**
- curl -s 'http://localhost:8080/api/orders/1?fields=id,status,total' | jq 'keys'
- curl -s 'http://localhost:8080/api/orders/1?fields=id,status,total' | jq 'length'
- grep -rn 'req.query.fields' src/ | head -10