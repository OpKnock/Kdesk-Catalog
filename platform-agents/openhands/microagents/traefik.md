---
name: "traefik"
description: "Run it and configure routers/services/middlewares."
type: knowledge
triggers: ["traefik", "traefik-routing"]
---

# Traefik

Run it and configure routers/services/middlewares.

## Instructions

# Traefik

Hand-crafted skill for edge routing with Traefik.

## What this skill does

- Boots Traefik with docker provider discovery
- Exposes routers and services via the HTTP API
- Verifies TLS and routing rules end to end

## When to use

- Adding a reverse proxy to a compose stack
- Inspecting which container serves which host rule
- Debugging 404s from bad router matchers

## Real commands

```bash
# Run with docker provider + API
docker run -d -p 80:80 -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock traefik:v3.0 --api.insecure=true

# Inspect state
curl -s localhost:8080/api/http/routers | jq
curl -s localhost:8080/api/http/services | jq

# Label-based routing on a container
docker run -d --label 'traefik.http.routers.app.rule=Host(`app.local`)' --label 'traefik.http.services.app.loadbalancer.server.port=80' nginx

# Verify
curl -sk https://localhost -H 'Host: app.local' -o /dev/null -w '%{http_code}'
```

## File provider config

```yaml
http:
  routers:
    app:
      rule: Host(`app.local`)
      service: app
      tls: {}
  services:
    app:
      loadBalancer:
        servers:
          - url: http://backend:3000
```

## Testing

```bash
curl -s localhost:8080/api/http/routers | jq '.[] | {name, rule}'
curl -sk https://localhost -H 'Host: app.local' -o /dev/null -w '%{http_code}'
```

## Best practices

- Use the file provider for production rules; docker labels for local
- Pin Traefik version tags; v3 changed labels syntax
- Enable access logging before debugging routing

## Capabilities

### traefik-routing
Run Traefik and configure routers/services/middlewares

**Commands:**
- `docker run -d -p 80:80 -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock traefik:v3.0 --api.insecure=true`
- `curl -s localhost:8080/api/http/routers | jq`
- `curl -s localhost:8080/api/http/services | jq`
- `docker service ls`
- `curl -sk https://localhost -H 'Host: app.local' -o /dev/null -w '%{http_code}'`

**Examples:**
- curl -s localhost:8080/api/http/routers | jq '.[] | {name, rule, service}'
- docker run -d -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock traefik:v3.0 --providers.docker=true
- curl -sk https://localhost -H 'Host: app.local' -o /dev/null -w '%{http_code}'
