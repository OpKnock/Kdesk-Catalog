---
name: "api-version-nginx-routing"
description: "Routes multiple API versions at the gateway: nginx location-based version routing, Traefik rules, and Kong services per version. Use when working with nginx version routing, kong service versions or when the user mentions nginx version routing, kong service versions."
license: "MIT"
compatibility: "Requires node.js, python, openapi, postman. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(deck:*) Bash(nginx:*)"
---

Routes multiple API versions at the gateway: nginx location-based version routing, Traefik rules, and Kong services per version.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nginx -t`, `curl -s -X POST http://localhost:8001/services -d 'name=user`
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

# API Version v5 - Gateway Routing

Gateway-level version routing.

## What This Skill Does
- Routes versioned paths to versioned backends
- Keeps versioning at the infrastructure layer
- Allows version-specific traffic control

## When to Use
- Multiple versioned backend deployments
- Canarying versions at the gateway
- Centralized version traffic management

## Real Commands

```bash
nginx -t
nginx -s reload
curl -s http://localhost:8080/v1/users -o /dev/null -w '%{http_code}\n'
curl -s -X POST http://localhost:8001/services -d 'name=users-v1' -d 'url=http://users-v1:8080'
```

## nginx Config

```nginx
location /v1/ {
  proxy_pass http://users-v1:8080/;
}
location /v2/ {
  proxy_pass http://users-v2:8080/;
}
```

## Testing
- Verify each version hits the right upstream
- Test unknown versions return 404
- Validate config before reload


## Best Practices
- Keep version routes explicit
- Add per-version rate limits
- Log version usage for sunset planning

## Capabilities

### nginx-version-routing
Route versioned paths with nginx

**Parameters:**
- `version` (string): Version path segment
- `upstream` (string): Backend upstream name
- `config` (string): nginx config path

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `curl -s http://localhost:8080/v1/users -o /dev/null -w '%{http_code}\n'`
- `curl -s http://localhost:8080/v2/users -o /dev/null -w '%{http_code}\n'`
- `curl -s http://localhost:8080/v9/users -o /dev/null -w '%{http_code}\n'`

**Examples:**
- location /v1/ proxies to the v1 upstream
- location /v2/ proxies to the v2 upstream
- nginx -s reload applies route changes

### kong-service-versions
Register versioned services in Kong

**Commands:**
- `curl -s -X POST http://localhost:8001/services -d 'name=users-v1' -d 'url=http://users-v1:8080'`
- `curl -s -X POST http://localhost:8001/services -d 'name=users-v2' -d 'url=http://users-v2:8080'`
- `curl -s -X POST http://localhost:8001/services/users-v1/routes -d 'paths[]=/v1/users'`
- `curl -s http://localhost:8000/v1/users -o /dev/null -w '%{http_code}\n'`
- `deck gateway sync kong.yaml`

**Examples:**
- -cli --help
- -api --help

## References
- [nginx location Docs](https://nginx.org/en/docs/http/ngx_http_core_module.html#location)
- [Kong Services and Routes](https://docs.konghq.com/gateway/latest/how-to/configure/services-and-routes/)
