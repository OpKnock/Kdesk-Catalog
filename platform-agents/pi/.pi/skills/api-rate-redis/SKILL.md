---
name: "api-rate-redis"
description: "Builds distributed rate limiting with Redis: shared counters across instances, ioredis clients, and Dockerized Redis for multi-node consistency. Use when working with redis setup, node integration or when the user mentions redis setup, node integration."
license: "MIT"
compatibility: "Requires redis, node.js, python, nginx, express-rate-limit."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(docker:*) Bash(node:*) Bash(npm:*) Bash(redis-cli:*)"
---

Builds distributed rate limiting with Redis: shared counters across instances, ioredis clients, and Dockerized Redis for multi-node consistency.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d -p 6379:6379 --name api-redis redis:7`, `redis-cli INCR rate:user:1 && redis-cli EXPIRE rate:user:1 6`
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
