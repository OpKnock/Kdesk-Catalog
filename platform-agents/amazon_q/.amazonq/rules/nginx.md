Configures and operates nginx servers: virtual hosts, TLS termination, log inspection, and zero-downtime reloads.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nginx -t`, `tail -f /var/log/nginx/error.log`
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

# Nginx

Configure and run nginx with confidence.

## When to Use

- Serving static content and reverse-proxying apps
- TLS termination and HTTP/2
- Diagnosing 4xx/5xx traffic patterns

## Virtual host

```nginx
server {
  listen 443 ssl http2;
  server_name api.example.com;

  ssl_certificate     /etc/nginx/ssl/fullchain.pem;
  ssl_certificate_key /etc/nginx/ssl/privkey.pem;

  location /api/ {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /static/ {
    alias /srv/static/;
    expires 7d;
    add_header Cache-Control 'public';
  }
}
```

## Safe reload loop

```bash
nginx -t
nginx -s reload
```

Always test before reload; a bad config leaves the old process running.

## Inspect effective config

```bash
nginx -T | grep -E 'server_name|listen'
```

## Log triage

```bash
tail -f /var/log/nginx/error.log
grep 'upstream timed out' /var/log/nginx/error.log | tail
```

Status-code distribution:

```bash
tail -n 1000 /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c | sort -rn
```

## Best practices

- Pin worker_processes to core count; enable keepalive to upstreams.
- Enable `gzip` and static asset caching for the web tier.
- Never serve `server_tokens off;` default leakage - hide version.
- Redirect HTTP to HTTPS at the server level, not per-location.

## Testing

```bash
nginx -t
curl -I http://localhost/static/app.js
```

Verify cache headers and TLS chain after each config change.

## Capabilities

### server
Manage nginx runtime: test, reload, and inspect.

**Parameters:**
- `c` (string): Config file path
- `s` (string): Signal: reload, reopen, stop, quit
- `T` (string): Dump full effective configuration

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `nginx -T`
- `nginx -v`
- `nginx -s stop`

**Examples:**
- nginx -t -c /etc/nginx/nginx.conf
- nginx -T | grep -E 'server_name|listen'
- nginx -s reload && nginx -v

### logs
Analyze access and error logs for issues.

**Parameters:**
- `log-file` (string): Path to access or error log
- `status-code` (string): HTTP status filter like 5xx
- `lines` (number): Number of lines to tail

**Commands:**
- `tail -f /var/log/nginx/error.log`
- `tail -n 100 /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c | sort -rn`
- `grep -E '5[0-9]{2}' /var/log/nginx/access.log | tail -20`
- `tail -f /var/log/nginx/access.log | grep -v ' 200 '`
- `awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10`

**Examples:**
- tail -f /var/log/nginx/error.log
- grep 'upstream timed out' /var/log/nginx/error.log | tail
- tail -n 1000 /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c | sort -rn

## References
- [nginx.org Docs](https://nginx.org/en/docs/)
- [nginx Beginner Guide](https://nginx.org/en/docs/beginners_guide.html)
- [nginx admin guide](https://nginx.org/en/docs/control.html)