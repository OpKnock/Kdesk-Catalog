---
name: "cache-strategy-architect"
description: "Architects caching systems end to end: CDN, reverse proxy, application cache, and database layers with coherence strategies. Use when working with layer caching, coherence design or when the user mentions layer caching, coherence design."
---

Architects caching systems end to end: CDN, reverse proxy, application cache, and database layers with coherence strategies.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -sI http://localhost:80/static/app.js`, `redis-cli publish cache.invalidate "user:123"`
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

# Cache Strategy Architect

Design coherent multi-layer caching.

## When to Use

- Designing cache layout for new or scaling systems
- Debugging stale reads across CDN/proxy/app/db caches
- Choosing TTL, validation, and invalidation strategies

## Layers

1. CDN: static assets, public edge content
2. Reverse proxy (nginx/varnish): shared public responses
3. Application cache (Redis/Memcached): hot data, sessions
4. Database cache: query results, read replicas

## Headers

- Cache-Control: max-age, s-maxage, no-store
- ETag: revalidation token
- Vary: key by Accept-Language, Authorization where needed

## Commands

```bash
# Inspect cache behavior
curl -sI http://localhost:80/static/app.js | grep -i cache
curl -s -o /dev/null -w "%{http_code} %{time_total}" http://localhost:80/api

# Coherence operations
redis-cli publish cache.invalidate "user:123"
redis-cli unlink user:123
redis-cli --scan --pattern "user:*"
redis-cli dbsize

# Proxy reload
nginx -t
nginx -s reload
```

## Best Practices

- Cache public data at the edge; private data in app cache only
- Use ETag revalidation over long TTLs for volatile content
- Invalidate by key pattern after writes, not just by TTL
- Add jitter to TTLs to avoid thundering herd
- Measure hit rates per layer before tuning
- Never cache sensitive responses without no-store

## Capabilities

### layer-caching
Design and operate CDN and reverse-proxy caching.

**Parameters:**
- `url` (string): URL to inspect cache headers for
- `header` (string): HTTP header to inspect (Cache-Control, ETag, Vary)

**Commands:**
- `curl -sI http://localhost:80/static/app.js`
- `curl -s -o /dev/null -w "%{http_code} %{time_total}" http://localhost:80/api`
- `nginx -t`
- `nginx -s reload`

**Examples:**
- curl -sI http://localhost:80/static/app.js | grep -i cache
- curl -s -o /dev/null -w "%{http_code}" -H "Cache-Control: max-age=0" http://localhost:80/api

### coherence-design
Design invalidation and write policies.

**Parameters:**
- `key` (string): Key to invalidate
- `pattern` (string): Key pattern to scan or invalidate

**Commands:**
- `redis-cli publish cache.invalidate "user:123"`
- `redis-cli unlink user:123`
- `redis-cli --scan --pattern "user:*"`
- `redis-cli dbsize`

**Examples:**
- redis-cli unlink "article:*"
- redis-cli publish cache.invalidate "orders:42"

## References
- [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [Redis Patterns](https://redis.io/docs/latest/develop/use/patterns/)
