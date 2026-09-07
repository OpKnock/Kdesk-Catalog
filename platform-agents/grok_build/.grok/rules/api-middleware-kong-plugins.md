Configures API gateway middleware using Kong Gateway and decK: global plugins like rate-limiting, key-auth, request-transformer, and CORS applied at the gateway edge.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d --name kong -p 8000:8000 -p 8443:8443 -p 8001:`, `curl -s http://localhost:8001/plugins -G --data-urlencode "n`
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