---
trigger: glob
description: "Builds distributed rate limiting with Redis: shared counters across instances, ioredis clients, and Dockerized Redis for multi-node consistency. Use when working with redis setup, node integration or when the user mentions redis setup, node integration."
globs: ["**/*.r", "**/*.sh"]
---

Builds distributed rate limiting with Redis: shared counters across instances, ioredis clients, and Dockerized Redis for multi-node consistency.

## Agentic Workflow: Read -> Reason -> Act (api-rate-redis)

You are **Api Rate Redis** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-rate-redis`
- Domain: Builds distributed rate limiting with Redis: shared counters across instances, ioredis clients, and Dockerized Redis for multi-node consistency.
- **redis-setup**: Run and connect to Redis for shared limit state — `docker run -d -p 6379:6379 --name api-redis redis:7`
- **node-integration**: Integrate Redis counting into a Node API — `redis-cli INCR rate:user:1 && redis-cli EXPIRE rate:user:1 60`
- Check `knowledge` and `prerequisites: redis, node.js, python`

### 2. Reason — think for `api-rate-redis`
- For `redis-setup`: Run and connect to Redis for shared limit state — decide which checks to run
- For `node-integration`: Integrate Redis counting into a Node API — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-rate-redis` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-rate-redis:1ef9c796`

# API Rate v2 - Redis Distributed

Distributed rate limiting with Redis.

## What This Skill Does
- Shares counters across all API instances
- Uses atomic INCR with TTL windows
- Survives instance restarts

## When to Use
- Multiple instances behind a load balancer
- Multi-region deployments needing shared limits
- Migration from in-memory to shared state

## Real Commands

```bash
docker run -d -p 6379:6379 --name api-redis redis:7
redis-cli ping
redis-cli INCR rate:user:1
redis-cli EXPIRE rate:user:1 60
```

## Atomic Middleware Pattern

```js
const Redis = require('ioredis');
const redis = new Redis({ host: 'redis', port: 6379 });
async function consume(key, limit, windowSec) {
  const count = await redis.incr(key);
  if (count === 1) await redis.expire(key, windowSec);
  return count <= limit;
}
```

## Testing
- Run two instances and confirm shared enforcement
- Kill Redis and verify fail-open/fail-closed policy
- Check memory with redis-cli --scan --pattern 'rate:*'

## Best Practices
- Use MULTI or Lua for check-and-set atomicity
- Namespace keys by environment
- Set conservative maxmemory with eviction policy

## Capabilities

### redis-setup
Run and connect to Redis for shared limit state

**Parameters:**
- `key` (string): Rate counter key name
- `expiry-seconds` (integer): TTL for the counter window
- `limit` (integer): Max requests per window

**Commands:**
- `docker run -d -p 6379:6379 --name api-redis redis:7`
- `redis-cli ping`
- `redis-cli -u redis://localhost:6379 GET rate:user:1`
- `npm install ioredis`
- `node -e "const Redis=require('ioredis'); const r=new Redis(); r.incr('rate:user:1').then(v=>{console.log(v); r.quit()})"`

**Examples:**
- redis-cli ping verifies connectivity
- INCR against the shared key counts across instances
- ioredis client runs Lua-free counter ops from Node

### node-integration
Integrate Redis counting into a Node API

**Commands:**
- `redis-cli INCR rate:user:1 && redis-cli EXPIRE rate:user:1 60`
- `redis-cli --scan --pattern 'rate:*'`
- `node -e "const Redis=require('ioredis'); const r=new Redis(); r.multi().incr('k').expire('k',60).exec().then(x=>{console.log(x); r.quit()})"`

**Examples:**
- -cli --help
- -api --help

## References
- [Redis Commands](https://redis.io/docs/latest/commands/incr/)
- [ioredis GitHub](https://github.com/redis/ioredis)
