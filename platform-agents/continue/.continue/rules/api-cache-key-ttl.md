---
name: "Api Cache Key Ttl"
description: "Designs cache architecture: TTL sizing, cache-key design, invalidation patterns, and multi-layer caching decisions. Use when working with key and ttl design, invalidation design or when the user mentions key and ttl design, invalidation design."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Designs cache architecture: TTL sizing, cache-key design, invalidation patterns, and multi-layer caching decisions.

## Agentic Workflow: Read -> Reason -> Act (api-cache-key-ttl)

You are **Api Cache Key Ttl** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `api-cache-key-ttl`
- Domain: Designs cache architecture: TTL sizing, cache-key design, invalidation patterns, and multi-layer caching decisions.
- **key-and-ttl-design**: Design cache keys and TTLs that match data volatility — `node -e "const key=['api','products','v2','42'].join(':');console.log(key)"`
- **invalidation-design**: Choose invalidation strategies: TTL, write-through, versioning, events — `redis-cli DEL api:products:v2:42`
- Check `knowledge` and `prerequisites: redis, node.js, python`

### 2. Reason — think for `api-cache-key-ttl`
- For `key-and-ttl-design`: Design cache keys and TTLs that match data volatility — decide which checks to run
- For `invalidation-design`: Choose invalidation strategies: TTL, write-through, versioning, events — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-cache-key-ttl` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-cache-key-ttl:d4baeb05`

# API Cache (Design)

Designs cache architecture before writing cache code.

## When to Use
- Planning caching for a new service
- Fixing stale-data incidents
- Deciding invalidation strategy

## Real Commands

```bash
# Key design
node -e "const key=['api','products','v2','42'].join(':');console.log(key)"

# TTL tiers
node -e "const tiers={hot:{ttl:60},warm:{ttl:300},cold:{ttl:3600}};console.log(JSON.stringify(tiers,null,2))"

# Version invalidation
redis-cli SET api:products:v2:42 '{}' EX 60 NX
redis-cli --scan --pattern 'api:products:v2:*' | xargs -r redis-cli DEL

# Event invalidation
redis-cli PUBLISH cache.invalidate '{"pattern":"api:products:*"}'
```

## Strategy Selection
- Volatile data: short TTL + events
- Stable data: long TTL, version keys
- Writes heavy: write-through

## Testing
Simulate an update and verify all affected keys are invalidated.

## Best Practices
- Version keys on schema changes
- Design invalidation before TTLs

## Capabilities

### key-and-ttl-design
Design cache keys and TTLs that match data volatility

**Parameters:**
- `resource` (string): Resource name
- `ttl` (string): TTL design

**Commands:**
- `node -e "const key=['api','products','v2','42'].join(':');console.log(key)"`
- `node -e "const tiers={hot:{ttl:60},warm:{ttl:300},cold:{ttl:3600}};console.log(JSON.stringify(tiers,null,2))"`
- `redis-cli SET api:products:v2:42 '{}' EX 60`
- `redis-cli --scan --pattern 'api:products:*'`
- `node -e "console.log('key parts: resource:version:id')"`

**Examples:**
- node -e "const key=['api','products','v2','42'].join(':');console.log(key)"
- node -e "const tiers={hot:{ttl:60},warm:{ttl:300},cold:{ttl:3600}};console.log(JSON.stringify(tiers,null,2))"
- redis-cli SET api:products:v2:42 '{}' EX 60

### invalidation-design
Choose invalidation strategies: TTL, write-through, versioning, events

**Parameters:**
- `pattern` (string): Invalidation pattern
- `strategy` (string): Invalidation strategy

**Commands:**
- `redis-cli DEL api:products:v2:42`
- `redis-cli --scan --pattern 'api:products:v2:*' | xargs -r redis-cli DEL`
- `redis-cli SET api:products:v2:42 '{}' EX 60 NX`
- `redis-cli PUBLISH cache.invalidate '{"pattern":"api:products:*"}'`
- `node -e "console.log('strategies: ttl | write-through | version | event')"`

**Examples:**
- redis-cli --scan --pattern 'api:products:v2:*' | xargs -r redis-cli DEL
- redis-cli SET api:products:v2:42 '{}' EX 60 NX
- redis-cli PUBLISH cache.invalidate '{"pattern":"api:products:*"}'

## References
- [Cache Invalidation](https://martinfowler.com/bliki/CacheInvalidation.html)
- [Redis NX Options](https://redis.io/docs/latest/commands/set/)