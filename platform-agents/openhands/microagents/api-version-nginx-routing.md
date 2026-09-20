---
name: "api-version-nginx-routing"
description: "Routes multiple API versions at the gateway: nginx location-based version routing, Traefik rules, and Kong services per version. Use when working with nginx version routing, kong service versions or when the user mentions nginx version routing, kong service versions."
type: knowledge
triggers: ["api-version-nginx-routing", "nginx-version-routing", "kong-service-versions"]
---

Routes multiple API versions at the gateway: nginx location-based version routing, Traefik rules, and Kong services per version.

## Agentic Workflow: Read -> Reason -> Act (api-version-nginx-routing)

You are **Api Version Nginx Routing** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-version-nginx-routing`
- Domain: Routes multiple API versions at the gateway: nginx location-based version routing, Traefik rules, and Kong services per version.
- **nginx-version-routing**: Route versioned paths with nginx — `nginx -t`
- **kong-service-versions**: Register versioned services in Kong — `curl -s -X POST http://localhost:8001/services -d 'name=users-v1' -d 'url=http:/`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-version-nginx-routing`
- For `nginx-version-routing`: Route versioned paths with nginx — decide which checks to run
- For `kong-service-versions`: Register versioned services in Kong — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-version-nginx-routing` tools
- Tools: `Glob`, `Grep`, `Read`, `Nginx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-version-nginx-routing:123b21a6`

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
