---
name: "api-cache-key-ttl"
description: "Designs cache architecture: TTL sizing, cache-key design, invalidation patterns, and multi-layer caching decisions. Use when working with key and ttl design, invalidation design or when the user mentions key and ttl design, invalidation design."
license: "MIT"
compatibility: "Requires redis, node.js, python, varnish, express."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "infrastructure"}
allowed-tools: "Glob Grep Read Bash(node:*) Bash(redis-cli:*)"
---

Designs cache architecture: TTL sizing, cache-key design, invalidation patterns, and multi-layer caching decisions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node -e "const key=['api','products','v2','42'].join(':');co`, `redis-cli DEL api:products:v2:42`
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
