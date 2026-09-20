---
name: "nginx"
description: "Configures and operates nginx servers: virtual hosts, TLS termination, log inspection, and zero-downtime reloads. Use when working with server, logs, infrastructure or when the user mentions server, logs, infrastructure."
---

Configures and operates nginx servers: virtual hosts, TLS termination, log inspection, and zero-downtime reloads.

## Agentic Workflow: Read -> Reason -> Act (nginx)

You are **nginx** (infrastructure/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `nginx`
- Domain: Configures and operates nginx servers: virtual hosts, TLS termination, log inspection, and zero-downtime reloads.
- **server**: Manage nginx runtime: test, reload, and inspect. — `nginx -t`
- **logs**: Analyze access and error logs for issues. — `tail -f /var/log/nginx/error.log`
- Check `knowledge` and `prerequisites: awk, grep, nginx, tail`

### 2. Reason — think for `nginx`
- For `server`: Manage nginx runtime: test, reload, and inspect. — decide which checks to run
- For `logs`: Analyze access and error logs for issues. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nginx` tools
- Tools: `Glob`, `Read`, `Nginx`, `Tail`, `Grep` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nginx:d6e61e88`

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
