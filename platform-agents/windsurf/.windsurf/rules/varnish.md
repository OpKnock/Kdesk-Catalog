---
trigger: glob
description: "Administers Varnish HTTP cache using VCL. Loads and reloads configurations, invalidates content with bans and purges, inspects hit rates via varnishstat, and debugs request routing with varnishlog. Use when working with varnish cache, api, http or when the user mentions varnish cache, api, http."
globs: ["**/*.html", "**/*.r", "**/*.sh"]
---

Administers Varnish HTTP cache using VCL. Loads and reloads configurations, invalidates content with bans and purges, inspects hit rates via varnishstat, and debugs request routing with varnishlog.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `varnishd -f /etc/varnish/default.vcl -s malloc,256m`
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

# Varnish

Hand-crafted skill for Varnish cache administration.

## What this skill does

- Loads and reloads VCL configs
- Invalidates cached content with bans and purges
- Reads hit rates and request logs

## When to use

- Tuning cache hit rate for an API or site
- Removing stale content after a release
- Debugging why a URL will not cache

## Real commands

```bash
# Start with a VCL and 256MB cache
varnishd -f /etc/varnish/default.vcl -s malloc,256m

# Reload VCL without dropping traffic
varnish_reload_vcl

# Ban (invalidate) matching objects
varnishadm ban "req.url ~ ^/products"
varnishadm ban "obj.http.x-cache-type ~ html"

# Stats
varnishstat -1 | grep -E "MAIN.cache_hit|MAIN.cache_miss|MAIN.hitmiss"

# Request log for one URL pattern
varnishlog -g request -q "ReqURL ~ /products"
```

## Minimal VCL

```vcl
vcl 4.0;
backend default { .host = "127.0.0.1"; .port = "8080"; }

sub vcl_backend_response {
  if (beresp.ttl <= 0s && bereq.method == "GET") {
    set beresp.ttl = 120s;
  }
  unset beresp.http.Set-Cookie;
}
```

## Testing

```bash
varnishstat -1 | grep "MAIN.cache_hit"   # hit count
varnishadm ban "req.url ~ ^/products"    # clear products
```

## Best practices

- Ban with narrow expressions; broad bans purge everything
- Never cache responses that carry Set-Cookie
- Watch hitmiss: it means miss then hit, a sign of warmup churn

## Capabilities

### varnish-cache
Manage VCL, purges, and cache stats

**Parameters:**
- `vcl_file` (string): Path to VCL config
- `ban_expression` (string): Ban regex, e.g. req.url ~ ^/products
- `cache_size` (string): malloc size, e.g. 256m

**Commands:**
- `varnishd -f /etc/varnish/default.vcl -s malloc,256m`
- `varnish_reload_vcl`
- `varnishadm ban "req.url ~ ^/products"`
- `varnishadm ban "obj.http.x-cache-type ~ html"`
- `varnishstat -1 | grep -E "MAIN.cache_hit|MAIN.cache_miss|MAIN.hitmiss"`
- `varnishlog -g request -q "ReqURL ~ /products"`

**Examples:**
- varnishadm ban "req.url ~ ^/products"
- varnishstat -1 | grep -E "MAIN.cache_hit|MAIN.cache_miss"
- varnish_reload_vcl

## References
- [Varnish VCL reference](https://varnish-cache.org/docs/trunk/reference/vcl.html)
- [Varnish CLI and stats](https://varnish-cache.org/docs/trunk/reference/varnishadm.html)
- [Varnish book](https://varnish-cache.org/docs/trunk/users-guide/index.html)
