---
name: "api-middleware-kong-plugins"
description: "Configures API gateway middleware using Kong Gateway and decK: global plugins like rate-limiting, key-auth, request-transformer, and CORS applied at the gateway edge. Use when working with kong plugins, plugin operations or when the user mentions kong plugins, plugin operations."
license: "MIT"
compatibility: "Requires node.js, python, express, fastify, koa. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(docker:*)"
---

Configures API gateway middleware using Kong Gateway and decK: global plugins like rate-limiting, key-auth, request-transformer, and CORS applied at the gateway edge.

## Agentic Workflow: Read -> Reason -> Act (api-middleware-kong-plugins)

You are **Api Middleware Kong Plugins** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-middleware-kong-plugins`
- Domain: Configures API gateway middleware using Kong Gateway and decK: global plugins like rate-limiting, key-auth, request-transformer, and CORS applied at the gateway edge.
- **kong-plugins**: Apply global and per-service middleware plugins on Kong Gateway — `docker run -d --name kong -p 8000:8000 -p 8443:8443 -p 8001:8001 kong/kong-gatew`
- **plugin-operations**: Inspect, update, and remove gateway middleware plugins via the Kong Admin API — `curl -s http://localhost:8001/plugins -G --data-urlencode "name=key-auth" | jq '`
- Check `knowledge` and `prerequisites: node.js, python, express, fastify`

### 2. Reason — think for `api-middleware-kong-plugins`
- For `kong-plugins`: Apply global and per-service middleware plugins on Kong Gateway — decide which checks to run
- For `plugin-operations`: Inspect, update, and remove gateway middleware plugins via the Kong Admin API — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-middleware-kong-plugins` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-middleware-kong-plugins:3d0e66ef`

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

**Parameters:**
- `plugin-name` (string): Kong plugin: rate-limiting, key-auth, cors, request-transformer
- `config` (object): Plugin-specific config (minute, allow list, header names)
- `scope` (string): Global, per-service, per-route, or per-consumer plugin scope

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

## References
- [Kong Gateway Plugins](https://docs.konghq.com/gateway/latest/reference/proxy-reference/)
- [decK Documentation](https://docs.konghq.com/deck/)
