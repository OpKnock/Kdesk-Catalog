---
applyTo: "**/*.r **/*.rs **/*.sh"
---

# Caddy

Serves sites and reverse proxies with Caddy: Caddyfile authoring, automatic HTTPS, file servers, and reloads.

## Instructions

# Caddy

## What this skill does

Serves sites and proxies with Caddy: Caddyfile authoring, automatic HTTPS with Let's Encrypt, static file serving, reverse proxying, and safe reloads.

## When to use

- Stand up a static site with HTTPS in seconds
- Reverse-proxy an API with automatic TLS
- Replacing nginx config complexity

## Real commands

```bash
# Serve static files
caddy file-server --root ./dist --listen :8080

# Reverse proxy
caddy reverse-proxy --from localhost:8080 --to localhost:3000

# Run with a Caddyfile
caddy run --config Caddyfile

# Validate before reload
caddy validate --config Caddyfile
caddy reload --config Caddyfile

# Format the Caddyfile
caddy fmt --overwrite Caddyfile
```

## Caddyfile example

```caddy
api.your-app.test {
  reverse_proxy localhost:3000
  encode gzip zstd
  header Cache-Control "max-age=3600"
}
```

## Testing

- caddy validate catches syntax errors pre-reload
- curl -sI to verify headers and certs

## Best practices

- Use caddy fmt for consistent formatting
- Keep Caddyfiles in version control; caddy reload is zero-downtime
- Let Caddy manage TLS; don't hand-manage certs unless needed

## Capabilities

### serve
Run Caddy as a file server or site server.

**Commands:**
- `caddy run`
- `caddy file-server --root ./public --listen :8080`
- `caddy reverse-proxy --from localhost:8080 --to localhost:3000`
- `caddy run --config Caddyfile`
- `caddy stop`

**Examples:**
- caddy file-server --root ./dist --listen :8080 --browse
- caddy reverse-proxy --from api.your-app.test --to localhost:3000
- caddy run --watch --config Caddyfile

### config
Validate and adapt Caddyfile configs.

**Commands:**
- `caddy validate --config Caddyfile`
- `caddy adapt --config Caddyfile`
- `caddy adapt --config Caddyfile --pretty`
- `caddy fmt Caddyfile`
- `caddy reload --config Caddyfile`

**Examples:**
- caddy validate --config Caddyfile
- caddy adapt --config Caddyfile --pretty > caddy.json
- caddy fmt --overwrite Caddyfile

### tls
Manage automatic HTTPS and certificates.

**Commands:**
- `caddy cert-manager list`
- `caddy trust`
- `caddy untrust`
- `curl -sI https://localhost:8443 | head -5`
- `caddy list-modules | grep tls`

**Examples:**
- caddy trust --ca /etc/caddy/ca.crt
- caddy cert-manager list --domain api.your-app.test
- caddy list-modules | grep -i tls
