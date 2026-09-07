---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Manages API gateways with Kong and decK: service/route registration, plugin policies, consumer credentials, and declarative configuration as code.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d --name kong -p 8000:8000 -p 8001:8001 kong/kon`, `deck ping`
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

**Parameters:**
- `service-name` (string): Upstream service name
- `upstream-url` (string): Backend URL
- `paths` (array): Route path patterns

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

## References
- [Kong Gateway Docs](https://docs.konghq.com/gateway/latest/)
- [decK Docs](https://docs.konghq.com/deck/)
