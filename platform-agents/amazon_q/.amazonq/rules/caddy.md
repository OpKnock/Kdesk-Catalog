Serves sites and reverse proxies with Caddy: Caddyfile authoring, automatic HTTPS, file servers, and reloads.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `caddy run`, `caddy validate --config Caddyfile`
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