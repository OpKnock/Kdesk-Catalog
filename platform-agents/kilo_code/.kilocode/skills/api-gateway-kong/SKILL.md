---
name: "api-gateway-kong"
description: "Implements API gateways hands-on: deploy Kong with deck, configure routes/services, and enable auth and rate-limit plugins. Use when working with kong operations, plugin configuration or when the user mentions kong operations, plugin configuration."
license: "MIT"
compatibility: "Requires kong, traefik, aws-cli, docker, kubernetes. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "infrastructure"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(deck:*) Bash(docker:*)"
---

Implements API gateways hands-on: deploy Kong with deck, configure routes/services, and enable auth and rate-limit plugins.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d --name kong-gateway -p 8000:8000 -p 8001:8001 `, `curl -s -X POST http://localhost:8001/services/orders/routes`
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
