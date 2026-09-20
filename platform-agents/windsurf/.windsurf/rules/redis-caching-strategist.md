---
trigger: glob
description: "Designs Redis caching strategies: TTL policies, invalidation, hit-rate measurement, and benchmark validation with redis-cli. Use when working with redis cli, benchmark or when the user mentions redis cli, benchmark."
globs: ["**/*.r", "**/*.sh"]
---

Designs Redis caching strategies: TTL policies, invalidation, hit-rate measurement, and benchmark validation with redis-cli.

## Agentic Workflow: Read -> Reason -> Act (redis-caching-strategist)

You are **redis-caching-strategist** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `redis-caching-strategist`
- Domain: Designs Redis caching strategies: TTL policies, invalidation, hit-rate measurement, and benchmark validation with redis-cli.
- **redis-cli**: Operate cache keys and measure health. — `redis-cli SET session:abc123 '{"user":42}' EX 900`
- **benchmark**: Validate cache performance with redis-benchmark. — `redis-benchmark -t set,get -n 100000 -c 50 -P 16`
- Check `knowledge` and `prerequisites: redis-cli, redis-benchmark, redis-sentinel, redis-cluster`

### 2. Reason — think for `redis-caching-strategist`
- For `redis-cli`: Operate cache keys and measure health. — decide which checks to run
- For `benchmark`: Validate cache performance with redis-benchmark. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-caching-strategist` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli`, `Redis-benchmark` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-caching-strategist:31271db1`

# Redis Caching Strategy

Design caches with measurable value.

## When to Use

- Hot reads on databases or APIs
- Session and rate-limit storage
- Distributed locks and rate limiting

## Cache-aside

```bash
redis-cli SET user:42 '{"name":"ada"}' EX 300
redis-cli GET user:42
```

Write path: update DB, then DELETE cache key (not write-through).

## TTL policy

- Short TTL for volatile data (sessions 15m).
- Long TTL for stable data (config 1h+).
- Add jitter to avoid thundering herd expiry.

## Hit rate

```bash
redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
```

hits / (hits + misses): target 80%+ for healthy caches.

## Stampede protection

```bash
redis-cli SETNX lock:key:42 worker-1 EX 30
```

Only the lock holder rebuilds the cache; others wait briefly.

## Validate performance

```bash
redis-benchmark -t set,get -n 100000 -c 50 -P 16
redis-cli --latency -h cache-1.example.com
```

## Best practices

- Never cache per-user data under global keys.
- Eviction policy: allkeys-lru for caches, noeviction for stores.
- Monitor memory, evictions, and hit rate.
- Preload cold caches before launches.

## Testing

Benchmark reads and measure hit rate before/after TTL changes.

## Capabilities

### redis-cli
Operate cache keys and measure health.

**Parameters:**
- `key` (string): Cache key
- `EX` (number): TTL seconds
- `pattern` (string): Key scan pattern

**Commands:**
- `redis-cli SET session:abc123 '{"user":42}' EX 900`
- `redis-cli TTL session:abc123`
- `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'`
- `redis-cli --scan --pattern 'cache:*' --count 1000 | head -20`
- `redis-cli MEMORY USAGE session:abc123`

**Examples:**
- redis-cli SETNX lock:order:42 worker-1 EX 30
- redis-cli INFO keyspace
- redis-cli --scan --pattern 'user:*' | wc -l

### benchmark
Validate cache performance with redis-benchmark.

**Parameters:**
- `test` (string): Command set like set,get,lpush
- `clients` (number): Concurrent clients
- `pipelining` (number): Pipelined requests per client

**Commands:**
- `redis-benchmark -t set,get -n 100000 -c 50 -P 16`
- `redis-benchmark -t lpush,incr -n 50000 -c 100 -d 128`
- `redis-benchmark -q -t set,get`
- `redis-cli --latency -h cache-1.example.com`
- `redis-cli --stat -i 1`

**Examples:**
- redis-benchmark -t set,get -n 100000 -c 50 -P 16 | grep -E 'SET|GET'
- redis-cli --latency --csv
- redis-benchmark -t get -n 200000 -c 100 -P 32 -d 256

## References
- [Redis Caching](https://redis.io/docs/latest/develop/use/patterns/caching/)
- [Redis Commands](https://redis.io/docs/latest/commands/)
- [redis-benchmark](https://redis.io/docs/latest/develop/reference/optimization/benchmarks/)
