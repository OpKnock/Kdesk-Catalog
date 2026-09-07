---
trigger: glob
description: "Implements API rate limiting with nginx limit_req and limit_conn modules: shared memory zones, burst queues, delayed processing, and 429 responses. Use when working with nginx limit req, limit conn or when the user mentions nginx limit req, limit conn."
globs: ["**/*.r", "**/*.sh"]
---

Implements API rate limiting with nginx limit_req and limit_conn modules: shared memory zones, burst queues, delayed processing, and 429 responses.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nginx -t`, `nginx -t -c /etc/nginx/nginx.conf`
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

# API Rate Engineer

Rate limiting with nginx.

## What This Skill Does
- Limits requests per second per client key
- Buffers bursts with queues or nodelay policy
- Limits concurrent connections per IP

## When to Use
- Protecting APIs behind nginx reverse proxy
- Throttling heavy endpoints without app changes
- Defending against single-IP abuse

## Real Commands

```bash
nginx -t
nginx -s reload
for i in $(seq 1 30); do curl -s -o /dev/null -w '%{http_code}\n' http://localhost/api/; done | sort | uniq -c
```

## Config Example

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
server {
  location /api/ {
    limit_req zone=api burst=20 nodelay;
    limit_req_status 429;
    proxy_pass http://backend;
  }
}
```

## Testing
- Fire over-limit bursts and count 429 responses
- Verify Retry-After headers appear on 429s
- Confirm normal traffic below the limit is unaffected

## Best Practices
- Key zones on real client identity, not just IP
- Use burst+nodelay for interactive APIs
- Log limit violations to a dedicated access log

## Capabilities

### nginx-limit-req
Configure request rate limiting zones in nginx

**Parameters:**
- `zone-name` (string): Zone identifier with size like api:10m
- `rate` (string): Rate like 10r/s or 60r/m
- `burst` (integer): Queue size for exceeded requests

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost/api/`
- `for i in $(seq 1 30); do curl -s -o /dev/null -w '%{http_code}\n' http://localhost/api/; done | sort | uniq -c`
- `curl -s -D- -o /dev/null http://localhost/api/ | grep -i retry-after`

**Examples:**
- limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s defines the zone
- limit_req zone=api burst=20 nodelay applies it to a location
- nginx -t validates config before reload

### limit-conn
Cap concurrent connections per client

**Commands:**
- `nginx -t -c /etc/nginx/nginx.conf`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost/api/health`
- `ab -n 500 -c 100 http://localhost/api/ 2>&1 | grep -i 'non-2xx'`

**Examples:**
- -cli --help
- -api --help

## References
- [nginx limit_req Module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
- [nginx limit_conn Module](https://nginx.org/en/docs/http/ngx_http_limit_conn_module.html)
