---
name: "Api Gateway Kong"
description: "Implements API gateways hands-on: deploy Kong with deck, configure routes/services, and enable auth and rate-limit plugins. Use when working with kong operations, plugin configuration or when the user mentions kong operations, plugin configuration."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Implements API gateways hands-on: deploy Kong with deck, configure routes/services, and enable auth and rate-limit plugins.

## Agentic Workflow: Read -> Reason -> Act (api-gateway-kong)

You are **Api Gateway Kong** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `api-gateway-kong`
- Domain: Implements API gateways hands-on: deploy Kong with deck, configure routes/services, and enable auth and rate-limit plugins.
- **kong-operations**: Deploy and configure Kong gateway with declarative configuration — `docker run -d --name kong-gateway -p 8000:8000 -p 8001:8001 kong/kong-gateway`
- **plugin-configuration**: Enable auth, rate limiting, and logging plugins on routes — `curl -s -X POST http://localhost:8001/services/orders/routes -H 'Content-Type: a`
- Check `knowledge` and `prerequisites: kong, traefik, aws-cli`

### 2. Reason — think for `api-gateway-kong`
- For `kong-operations`: Deploy and configure Kong gateway with declarative configuration — decide which checks to run
- For `plugin-configuration`: Enable auth, rate limiting, and logging plugins on routes — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-gateway-kong` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Deck` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-gateway-kong:03d79b49`

# API Gateway (Implementation)

Deploys and operates Kong API gateways with declarative config.

## When to Use
- Centralizing API entry points
- Adding auth and rate limits without app changes
- Multi-service routing

## Real Commands

```bash
# Run Kong
kong migrations bootstrap
kong start
docker run -d --name kong-gateway -p 8000:8000 -p 8001:8001 kong/kong-gateway

# Declarative config
deck ping
kong config -c kong.yaml

# Add a route
curl -s -X POST http://localhost:8001/services/orders/routes -H 'Content-Type: application/json' -d '{"paths":["/orders"]}'

# Plugins
curl -s -X POST http://localhost:8001/services/orders/plugins -H 'Content-Type: application/json' -d '{"name":"rate-limiting","config":{"minute":60}}'
```

## Testing
Send requests through the gateway and verify 401/429 behavior after enabling plugins.

## Best Practices
- Keep config in Git via deck sync
- Enable rate limiting before going public
- Use health checks on upstreams

## Capabilities

### kong-operations
Deploy and configure Kong gateway with declarative configuration

**Parameters:**
- `service` (string): Upstream service name
- `route` (string): Route path or host

**Commands:**
- `docker run -d --name kong-gateway -p 8000:8000 -p 8001:8001 kong/kong-gateway`
- `deck ping`
- `deck dump --output-file kong.yaml`
- `deck sync --state kong.yaml`
- `curl -s http://localhost:8001/status`

**Examples:**
- deck ping && deck dump --output-file kong.yaml
- deck sync --state kong.yaml
- curl -s http://localhost:8001/services | python -m json.tool

### plugin-configuration
Enable auth, rate limiting, and logging plugins on routes

**Parameters:**
- `plugin` (string): Plugin name
- `config` (string): Plugin configuration JSON

**Commands:**
- `curl -s -X POST http://localhost:8001/services/orders/routes -H 'Content-Type: application/json' -d '{"paths":["/orders"]}'`
- `curl -s -X POST http://localhost:8001/services/orders/plugins -H 'Content-Type: application/json' -d '{"name":"rate-limiting","config":{"minute":60}}'`
- `curl -s -X POST http://localhost:8001/services/orders/plugins -H 'Content-Type: application/json' -d '{"name":"jwt"}'`
- `curl -s -X POST http://localhost:8001/services/orders/plugins -H 'Content-Type: application/json' -d '{"name":"http-log","config":{"http_endpoint":"http://logs:8080"}}'`
- `curl -s http://localhost:8001/services/orders/plugins | python -m json.tool`

**Examples:**
- curl -s -X POST http://localhost:8001/services/orders/plugins -H 'Content-Type: application/json' -d '{"name":"rate-limiting","config":{"minute":60}}'
- curl -s -X POST http://localhost:8001/services/orders/plugins -H 'Content-Type: application/json' -d '{"name":"jwt"}'
- curl -s http://localhost:8001/services/orders/plugins | python -m json.tool

## References
- [Kong Gateway Docs](https://docs.konghq.com/gateway/)
- [deck CLI](https://docs.konghq.com/deck/)