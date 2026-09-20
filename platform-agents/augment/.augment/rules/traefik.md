---
type: agent_requested
description: "Run it and configure routers/services/middlewares. Use when working with traefik routing, api or when the user mentions traefik routing, api."
---

Run it and configure routers/services/middlewares.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d -p 80:80 -p 8080:8080 -v /var/run/docker.sock:`
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

**Parameters:**
- `rule` (string): Host/Path matcher, e.g. Host(`app.local`)
- `provider` (string): docker, file, or kubernetescrd
- `entrypoint` (string): web or websecure

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

## References
- [Traefik Docker provider](https://doc.traefik.io/traefik/providers/docker/)
- [Traefik API](https://doc.traefik.io/traefik/operations/api/)