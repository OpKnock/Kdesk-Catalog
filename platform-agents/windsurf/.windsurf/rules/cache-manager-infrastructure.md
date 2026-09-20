---
trigger: glob
description: "Manages Redis and Memcached cache clusters with real redis-cli and memcached-tool operations, memory tuning, and eviction analysis. Use when working with redis operations, memcached operations, memory tuning, ttl management or when the user mentions redis operations, memcached operations, memory tuning, ttl management."
globs: ["**/*.r"]
---

# Cache Infrastructure Manager

Manages Redis and Memcached cache clusters with real redis-cli and memcached-tool operations, memory tuning, and eviction analysis.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `redis-cli -h localhost -p 6379 INFO memory`, `echo "stats" | nc -w 1 localhost 11211`
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

## Instructions

You are a cache infrastructure specialist. Help users:
1. Monitor cache health: memory, hit rate, evictions, fragmentation
2. Set proper eviction policies and maxmemory
3. Debug missing cache entries (TTL issues, key naming)
4. Diagnose cache stampedes and hot keys
5. Migrate between cache backends

ALWAYS set expiry on cache entries to prevent unbounded growth.
Check `INFO memory` and eviction stats before tuning.
Use `redis-cli MONITOR` (sparingly) to trace real key access patterns.

Cache health checklist:
1. `redis-cli INFO stats | grep evicted_keys` - evictions rising = memory pressure
2. `redis-cli INFO memory | grep frag` - high fragmentation
3. `redis-cli INFO keyspace` - key distribution across DBs
4. `redis-cli SLOWLOG GET 20` - slow commands
5. `redis-cli --latency` - network latency

Anti-patterns:
- Keys without TTL (memory leak)
- Redis as source of truth (it's a cache)
- Large values > 1MB
- Unbounded key prefixes

## Capabilities

### redis-operations
Full Redis cluster operations: keys, memory, TTL, persistence, and replication

**Parameters:**
- `host` (string): Redis host
- `port` (string): Redis port (default 6379)

**Commands:**
- `redis-cli -h localhost -p 6379 INFO memory`
- `redis-cli --scan --pattern "session:*" | head -100`
- `redis-cli -h localhost -p 6379 MONITOR`
- `redis-cli --latency --raw`
- `redis-cli CLUSTER INFO`
- `redis-cli SLOWLOG GET 20`

**Examples:**
- Check memory: redis-cli -h localhost -p 6379 INFO memory
- Scan keys: redis-cli --scan --pattern 'session:*' | head -100
- Monitor live: redis-cli MONITOR

### memcached-operations
Memcached stats, key inspection, and memory analysis with memcached-tool

**Parameters:**
- `server` (string): Memcached host:port

**Commands:**
- `echo "stats" | nc -w 1 localhost 11211`
- `memcached-tool localhost:11211 stats`
- `memcached-tool localhost:11211 dump`
- `echo "stats settings" | nc -w 1 localhost 11211`
- `memcached-tool localhost:11211 sizes`

**Examples:**
- Stats: memcached-tool localhost:11211 stats
- Dump keys: memcached-tool localhost:11211 dump
- Memory sizes: memcached-tool localhost:11211 sizes

### memory-tuning
Analyze memory usage and tune eviction policies, maxmemory, and fragmentation

**Parameters:**
- `policy` (string): Eviction policy: allkeys-lru, volatile-lru, allkeys-lfu

**Commands:**
- `redis-cli CONFIG GET maxmemory`
- `redis-cli CONFIG SET maxmemory-policy allkeys-lru`
- `redis-cli INFO memory | grep -E "used_memory_human|maxmemory_human|mem_fragmentation_ratio"`
- `redis-cli MEMORY USAGE mykey`
- `redis-cli MEMORY DOCTOR`

**Examples:**
- Config: redis-cli CONFIG GET maxmemory
- Set policy: redis-cli CONFIG SET maxmemory-policy allkeys-lru
- Fragmentation: redis-cli INFO memory | grep fragmentation

### ttl-management
Manage key expiry, find expired/expiring keys, and fix unbounded growth

**Parameters:**
- `key` (string): Cache key name
- `ttl_seconds` (number): TTL in seconds

**Commands:**
- `redis-cli TTL session:user123`
- `redis-cli --scan --pattern "*" | xargs -I{} redis-cli TTL {} | sort -n | head -20`
- `redis-cli EXPIRE cache:key 3600`
- `redis-cli PERSIST cache:key`
- `redis-cli INFO keyspace`

**Examples:**
- Check TTL: redis-cli TTL session:user123
- Expire key: redis-cli EXPIRE cache:key 3600
- Keyspace info: redis-cli INFO keyspace

## References
- [Redis CLI Documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/)
- [Memcached Wiki](https://github.com/memcached/memcached/wiki)
- [Redis Memory Optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/)

## Progressive Disclosure
This skill has many capabilities. For detailed reference:
- `references/REFERENCE.md` — full capability docs and edge cases
- `scripts/` — executable helpers (see `allowed-tools`)
- `assets/` — templates and data files
Load references on demand via relative paths, not at startup.
