# Api Rate Redis

Builds distributed rate limiting with Redis: shared counters across instances, ioredis clients, and Dockerized Redis for multi-node consistency.

## Instructions

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
