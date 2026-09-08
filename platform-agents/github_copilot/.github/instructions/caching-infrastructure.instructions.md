---
applyTo: "**/*.r **/*.sh"
---

Operates Redis and Varnish caches: cache-aside patterns, invalidation, hit-rate analysis, and ban/purge workflows.

## Agentic Workflow: Read -> Reason -> Act (caching-infrastructure)

You are **caching-infrastructure** (infrastructure/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `caching-infrastructure`
- Domain: Operates Redis and Varnish caches: cache-aside patterns, invalidation, hit-rate analysis, and ban/purge workflows.
- **redis**: Manage cache keys, TTLs, and hit rates in Redis. — `redis-cli SET user:42 '{"name":"ada"}' EX 300`
- **varnish**: Inspect and purge content on Varnish caches. — `varnishstat -1 | grep -E 'MAIN.cache_hit|MAIN.cache_miss'`
- Check `knowledge` and `prerequisites: redis-cli, varnishadm, varnishstat`

### 2. Reason — think for `caching-infrastructure`
- For `redis`: Manage cache keys, TTLs, and hit rates in Redis. — decide which checks to run
- For `varnish`: Inspect and purge content on Varnish caches. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `caching-infrastructure` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli`, `Varnishstat` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `caching-infrastructure:0a884fca`

# Caching

Design and operate caches with measurable hit rates and safe invalidation.

## When to Use

- Hot reads hitting the database repeatedly
- Reducing origin load for public content
- Session or rate-limit storage

## Cache-aside with Redis

1. Read: `GET user:42` -> miss -> load DB -> `SET user:42 ... EX 300`.
2. Write: update DB -> `DEL user:42` (or set new value).

```bash
redis-cli SET user:42 '{"name":"ada"}' EX 300
redis-cli GET user:42
```

Never write-through without a TTL plan - stale keys become permanent.

## Measure hit rate

```bash
redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
```

Compute `hits / (hits + misses)`; below 80% means keys are too short-lived or poorly selected.

## Varnish invalidation

```bash
varnishadm -S /etc/varnish/secret -T 127.0.0.1:6082 ban 'req.url ~ ^/products'
```

Bans are async and cheap: the object is purged on next fetch.

## Cache stampede prevention

- Lock the rebuild: only one worker fills the key (`SET NX EX`).
- Add jitter to TTLs to avoid synchronized expiry.
- Use stale-while-revalidate for degraded mode.

## Best practices

- Never cache user-specific data globally; namespace by id.
- Set a cache policy header on every response.
- Purge on publish, not on a cron schedule.
- Monitor hit rate per key pattern, not just globally.

## Testing

```bash
redis-cli --scan --pattern 'user:*' | wc -l
varnishstat -1 | grep -E 'MAIN.cache_hit'
```

Assert expected TTLs and hit rates after load tests.

## Capabilities

### redis
Manage cache keys, TTLs, and hit rates in Redis.

**Parameters:**
- `key` (string): Cache key to operate on
- `EX` (number): TTL in seconds
- `pattern` (string): Glob pattern for key scans

**Commands:**
- `redis-cli SET user:42 '{"name":"ada"}' EX 300`
- `redis-cli TTL user:42`
- `redis-cli --scan --pattern 'user:*' --count 1000`
- `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'`
- `redis-cli DEL user:42`

**Examples:**
- redis-cli SET session:abc 1 EX 900 NX
- redis-cli INFO keyspace
- redis-cli --scan --pattern 'feed:*' | xargs -r redis-cli DEL

### varnish
Inspect and purge content on Varnish caches.

**Parameters:**
- `secret` (string): Varnish CLI secret file
- `ban` (string): VCL condition to invalidate matching objects
- `n` (string): Cache instance name

**Commands:**
- `varnishstat -1 | grep -E 'MAIN.cache_hit|MAIN.cache_miss'`
- `varnishadm -S /etc/varnish/secret -T 127.0.0.1:6082 ban 'req.url ~ ^/api'`
- `varnishadm -S /etc/varnish/secret -T 127.0.0.1:6082 ban 'obj.http.x-host == "www.example.com"'`
- `varnishadm -S /etc/varnish/secret -T 127.0.0.1:6082 purge.all`
- `curl -I http://localhost:8080/ -H 'Cache-Control: no-cache'`

**Examples:**
- varnishadm -S /etc/varnish/secret -T 127.0.0.1:6082 ban 'req.url ~ ^/products/[0-9]+'
- varnishlog -q 'RespStatus >= 500' -d -n cache-1 | head -50
- varnishstat -1 | grep -i hit

## References
- [Redis Caching Patterns](https://redis.io/docs/latest/develop/use/patterns/caching/)
- [Varnish Docs](https://varnish-cache.org/docs/)
- [Varnish Cache Hits](https://www.varnish-software.com/developers/tutorials/hitmiss-hithit-misshit/)
