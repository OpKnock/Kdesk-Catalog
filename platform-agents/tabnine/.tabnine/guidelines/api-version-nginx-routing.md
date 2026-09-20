# Api Version Nginx Routing

Routes multiple API versions at the gateway: nginx location-based version routing, Traefik rules, and Kong services per version.

## Instructions

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