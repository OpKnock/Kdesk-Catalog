---
type: agent_requested
description: "Implements API caching end to end: HTTP caching headers, Express/FastAPI middleware, and Redis cache-aside."
---

# Api Cache Middleware Implementation

Implements API caching end to end: HTTP caching headers, Express/FastAPI middleware, and Redis cache-aside.

## Instructions

# API Cache (Implementation)

Implements caching layers in the API stack with minimal code changes.

## When to Use
- Adding caching to an existing API quickly
- Protecting the database from repeated reads
- Getting HTTP caching right the first time

## Real Commands

```bash
# Node caching
npm install apicache
node -e "const ac=require('apicache');const mw=ac.middleware('5 minutes');console.log(typeof mw)"

# Python caching
pip install fastapi-cache2

# Cache-aside store
redis-cli SET api:products:42 '{"id":42}' EX 300
redis-cli TTL api:products:42
redis-cli DEL api:products:42
```

## Cache-aside Flow
1. Check Redis: `redis-cli GET api:products:42`
2. On miss, read DB, then `SET ... EX 300`
3. On write, `DEL api:products:42`

## Testing
Hit the endpoint twice and confirm the second read skips the DB (check query logs).

## Best Practices
- Start with 5-10 minute TTLs
- Always set Cache-Control on responses
- Never cache writes or 4xx responses

## Capabilities

### middleware-implementation
Add caching middleware to Node and Python APIs

**Commands:**
- `npm install apicache`
- `npm install express-cache-middleware`
- `pip install cachetools`
- `pip install fastapi-cache2`
- `npm install memory-cache`

**Examples:**
- npm install apicache && node -e "const ac=require('apicache');const mw=ac.middleware('5 minutes');console.log(typeof mw)"
- pip install fastapi-cache2 && python -c "from fastapi_cache import FastAPICache; print('ok')"
- npm install express-cache-middleware && node -e "const C=require('express-cache-middleware');const c=new C();console.log(typeof c.attach)"

### redis-cache-aside
Implement cache-aside with TTL and explicit invalidation on writes

**Commands:**
- `redis-cli SET api:products:42 '{"id":42}' EX 300`
- `redis-cli GET api:products:42`
- `redis-cli TTL api:products:42`
- `redis-cli DEL api:products:42`
- `redis-cli EXISTS api:products:42`

**Examples:**
- redis-cli SET api:products:42 '{"id":42}' EX 300 && redis-cli TTL api:products:42
- redis-cli GET api:products:42 || curl -s http://localhost:3000/api/products/42
- redis-cli DEL api:products:42 && redis-cli EXISTS api:products:42