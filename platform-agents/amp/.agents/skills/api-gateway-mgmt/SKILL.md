---
name: "api-gateway-mgmt"
description: "Manages API gateways with Kong and decK: service/route registration, plugin policies, consumer credentials, and declarative configuration as code."
---

# Api Gateway Mgmt

Manages API gateways with Kong and decK: service/route registration, plugin policies, consumer credentials, and declarative configuration as code.

## Instructions

# API Gateway Management

Gateway administration with Kong/decK.

## What This Skill Does
- Registers services, routes, and plugins
- Manages config as code with decK
- Applies gateway policies centrally

## When to Use
- Central API routing
- Gateway-level auth and rate limits
- Reproducible gateway configs

## Real Commands

```bash
docker run -d --name kong -p 8000:8000 -p 8001:8001 kong/kong-gateway
curl -s -X POST http://localhost:8001/services -d 'name=users' -d 'url=http://users-svc:8080'
curl -s -X POST http://localhost:8001/services/users/routes -d 'paths[]=/users'
curl -s -X POST http://localhost:8001/plugins -d 'name=rate-limiting' -d 'config.minute=60'
```

## Declarative Flow
1. deck gateway dump to capture current state
2. Edit kong.yaml in version control
3. deck gateway diff to preview changes
4. deck gateway sync to apply

## Testing
- Verify routes resolve through the gateway
- Test plugin enforcement
- Validate YAML before sync


## Best Practices
- Prefer declarative config over ad-hoc API calls
- Scope plugins to routes or services
- Version gateway configs with the codebase

## Capabilities

### kong-admin
Manage Kong services, routes, and plugins

**Commands:**
- `docker run -d --name kong -p 8000:8000 -p 8001:8001 kong/kong-gateway`
- `curl -s -X POST http://localhost:8001/services -d 'name=users' -d 'url=http://users-svc:8080'`
- `curl -s -X POST http://localhost:8001/services/users/routes -d 'paths[]=/users'`
- `curl -s -X POST http://localhost:8001/plugins -d 'name=rate-limiting' -d 'config.minute=60'`
- `curl -s http://localhost:8001/services | jq '.data[].name'`

**Examples:**
- POST /services registers an upstream
- POST /services/:name/routes maps paths
- POST /plugins applies gateway policies

### deck-config
Manage Kong configuration as code

**Commands:**
- `deck ping`
- `deck gateway dump -o kong.yaml`
- `deck gateway diff kong.yaml`
- `deck gateway sync kong.yaml`
- `deck gateway validate kong.yaml`

**Examples:**
- general-cli --help
- general-api --help
