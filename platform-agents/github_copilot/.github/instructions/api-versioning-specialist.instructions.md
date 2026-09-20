---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

# api-versioning-specialist

Specializes in media-type and header API versioning: vendor MIME types, Accept header negotiation, Vary handling, and version metadata in responses.

## Instructions

# API Versioning Specialist

Media-type and header versioning.

## What This Skill Does
- Negotiates versions through Accept headers
- Uses vendor MIME types and date headers
- Handles caching with Vary

## When to Use
- Public APIs requiring fine-grained versioning
- APIs where URLs must stay stable
- Caching layers with content negotiation

## Real Commands

```bash
curl -s -H 'Accept: application/vnd.myapi.v1+json' https://api.example.com/orders | jq '.meta.version'
curl -s -H 'X-API-Version: 2024-06-01' https://api.example.com/orders | jq '.meta.version'
curl -s -D- -H 'Accept: application/vnd.myapi.v2+json' https://api.example.com/orders | grep -i '^vary:'
```

## Header Strategy
- Vendor media type: application/vnd.api.v2+json
- Date-based: X-API-Version: 2024-06-01
- Query: ?api-version=2 (fallback)

## Testing
- Test each negotiation path
- Verify Vary headers on cached responses
- Confirm 406 for unknown versions


## Best Practices
- Set Vary: Accept to protect caches
- Prefer explicit version over defaults
- Document version selection for clients

## Capabilities

### media-type-versioning
Negotiate versions via media types

**Commands:**
- `curl -s -H 'Accept: application/vnd.myapi.v1+json' http://localhost:8080/orders | jq '.meta.version'`
- `curl -s -H 'Accept: application/vnd.myapi.v2+json' http://localhost:8080/orders | jq '.meta.version'`
- `curl -s -D- -H 'Accept: application/vnd.myapi.v2+json' http://localhost:8080/orders | grep -i '^vary:'`
- `curl -s -H 'Accept: application/json' http://localhost:8080/orders -o /dev/null -w '%{http_code}\n'`

**Examples:**
- Vendor media types carry the version
- Vary: Accept keeps caches honest
- Unversioned Accept can default or 406

### header-versioning
Use custom headers for version selection

**Commands:**
- `curl -s -H 'X-API-Version: 2024-06-01' http://localhost:8080/orders | jq '.meta.version'`
- `curl -s -H 'API-Version: 2' http://localhost:8080/orders | jq '.apiVersion'`
- `curl -s -o /dev/null -w '%{http_code}\n' -H 'X-API-Version: 1990-01-01' http://localhost:8080/orders`

**Examples:**
- -cli --help
- -api --help
