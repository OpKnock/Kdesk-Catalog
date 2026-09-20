---
name: "Api Middleware Kong Plugins"
description: "Configures API gateway middleware using Kong Gateway and decK: global plugins like rate-limiting, key-auth, request-transformer, and CORS applied at the gateway edge."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

# Api Middleware Kong Plugins

Configures API gateway middleware using Kong Gateway and decK: global plugins like rate-limiting, key-auth, request-transformer, and CORS applied at the gateway edge.

## Instructions

# API Middleware v5 - Gateway Edge

Middleware implemented as Kong Gateway plugins.

## What This Skill Does
- Applies rate limiting, key-auth, CORS, and request transformation at the gateway
- Manages plugins as declarative config with decK
- Moves cross-cutting concerns out of service code

## When to Use
- Centralizing auth and throttling across many services
- Applying CORS at the edge instead of per service
- Auditing middleware config in version control

## Real Commands

```bash
docker run -d --name kong -p 8000:8000 -p 8001:8001 kong/kong-gateway
curl -s -X POST http://localhost:8001/plugins -d 'name=rate-limiting' -d 'config.minute=60'
curl -s -X POST http://localhost:8001/plugins -d 'name=key-auth'
```

## Plugin Operations
- Filter plugins by name with --data-urlencode
- Update config in place with PATCH
- Remove plugins with DELETE

## Testing
- POST to /plugins then hit the proxy route to observe 429 or 401
- Run deck gateway diff before syncing changes
- Verify plugin order matches execution phases (auth before rate-limit)

## Best Practices
- Prefer decK files over Admin API mutations for reproducibility
- Scope plugins per route when global behavior differs
- Keep secrets out of declarative config via vault references

## Capabilities

### kong-plugins
Apply global and per-service middleware plugins on Kong Gateway

**Commands:**
- `docker run -d --name kong -p 8000:8000 -p 8443:8443 -p 8001:8001 kong/kong-gateway`
- `curl -s http://localhost:8001/plugins | jq '.data | length'`
- `curl -s -X POST http://localhost:8001/plugins -d 'name=rate-limiting' -d 'config.minute=60'`
- `curl -s -X POST http://localhost:8001/plugins -d 'name=key-auth'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/api`

**Examples:**
- curl -s -X POST localhost:8001/plugins -d 'name=rate-limiting' -d 'config.minute=60' applies global limits
- deck gateway sync kong.yaml applies plugins from declarative config
- curl -s localhost:8001/plugins returns installed gateway middleware

### plugin-operations
Inspect, update, and remove gateway middleware plugins via the Kong Admin API

**Commands:**
- `curl -s http://localhost:8001/plugins -G --data-urlencode "name=key-auth" | jq '.data[0] | {name, enabled}'`
- `curl -s -X PATCH http://localhost:8001/plugins/$(curl -s http://localhost:8001/plugins | jq -r '.data[0].id') -d 'config.minute=120'`
- `curl -s -X DELETE http://localhost:8001/plugins/$(curl -s http://localhost:8001/plugins | jq -r '.data[0].id') -o /dev/null -w '%{http_code}\n'`
- `curl -s http://localhost:8001/plugins -o /dev/null -w '%{http_code}\n'`

**Examples:**
- curl with --data-urlencode filters plugins by name
- PATCH updates plugin config in place
- DELETE removes a middleware plugin