---
name: "api-gateway-kong"
description: "Implements API gateways hands-on: deploy Kong with deck, configure routes/services, and enable auth and rate-limit plugins."
type: knowledge
triggers: ["api-gateway-kong", "kong-operations", "plugin-configuration"]
---

# Api Gateway Kong

Implements API gateways hands-on: deploy Kong with deck, configure routes/services, and enable auth and rate-limit plugins.

## Instructions

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
