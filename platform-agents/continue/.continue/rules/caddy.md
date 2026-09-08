---
name: "Caddy"
description: "Serves sites and reverse proxies with Caddy: Caddyfile authoring, automatic HTTPS, file servers, and reloads. Use when working with serve, config, tls, api or when the user mentions serve, config, tls, api."
globs: ["**/*.r", "**/*.rs", "**/*.sh"]
alwaysApply: false
---

Serves sites and reverse proxies with Caddy: Caddyfile authoring, automatic HTTPS, file servers, and reloads.

## Agentic Workflow: Read -> Reason -> Act (caddy)

You are **Caddy** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `caddy`
- Domain: Serves sites and reverse proxies with Caddy: Caddyfile authoring, automatic HTTPS, file servers, and reloads.
- **serve**: Run Caddy as a file server or site server. — `caddy run`
- **config**: Validate and adapt Caddyfile configs. — `caddy validate --config Caddyfile`
- **tls**: Manage automatic HTTPS and certificates. — `caddy cert-manager list`
- Check `knowledge` and `prerequisites: caddy`

### 2. Reason — think for `caddy`
- For `serve`: Run Caddy as a file server or site server. — decide which checks to run
- For `config`: Validate and adapt Caddyfile configs. — decide which checks to run
- For `tls`: Manage automatic HTTPS and certificates. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `caddy` tools
- Tools: `Glob`, `Grep`, `Read`, `Caddy`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `caddy:aca2a9bd`

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

**Parameters:**
- `root` (string): Document root
- `listen` (string): Listen address
- `config` (string): Caddyfile path

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

**Parameters:**
- `config` (string): Caddyfile path
- `pretty` (boolean): Pretty-print adapted JSON

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

**Parameters:**
- `domain` (string): Domain for cert management
- `ca` (string): CA file path

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

## References
- [Caddy Docs](https://caddyserver.com/docs/)
- [Caddy CLI Reference](https://caddyserver.com/docs/command-line)