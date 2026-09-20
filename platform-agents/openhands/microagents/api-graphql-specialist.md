---
name: "api-graphql-specialist"
description: "Deep GraphQL expertise: query planning, cost analysis, persisted queries, caching, and advanced security hardening."
type: knowledge
triggers: ["api-graphql-specialist", "query-security", "performance-debugging"]
---

# api-graphql-specialist

Deep GraphQL expertise: query planning, cost analysis, persisted queries, caching, and advanced security hardening.

## Instructions

# API GraphQL Specialist

Deep expertise in running GraphQL at scale: security, performance, and client efficiency.

## When to Use
- Expensive or abusive queries
- N+1 and slow-resolver issues
- Hardening GraphQL in production

## Real Commands

```bash
# Cost analysis
npm install graphql-query-complexity

# Hardening bundle
npm install @escape.tech/graphql-armor

# Benchmark a query
curl -s -X POST http://localhost:4001/graphql -H 'Content-Type: application/json' -d '{"query":"{ products { id name } }"}' -w '\n%{time_total}s'

# Schema audits
graphql-inspector audit docs/query.graphql schema.graphql
```

## Security Config
- `maxDepth: 10` — reject deep nesting
- `maxCost: 1000` — reject expensive queries
- Persisted queries to shrink attack surface

## Performance Playbook
1. Reproduce with curl timing
2. Add DataLoader for batch reads
3. Cache resolvers by field and TTL
4. Re-benchmark and compare

## Best Practices
- Reject unknown queries in production
- Log slow queries above a threshold
- Run schema audit in CI

## Capabilities

### query-security
Protect GraphQL APIs with complexity limits, depth limits, and persisted queries

**Commands:**
- `npm install graphql-cost-analysis`
- `node -e "const {costAnalysisPlugin}=require('@graphql-community/graphql-query-cost');console.log(typeof costAnalysisPlugin)"`
- `npm install @escape.tech/graphql-armor`
- `node -e "const a=require('@escape.tech/graphql-armor');console.log(Object.keys(a))"`
- `npm install graphql-query-complexity`

**Examples:**
- npm install graphql-query-complexity && node -e "const c=require('graphql-query-complexity');console.log(typeof c)"
- npm install @escape.tech/graphql-armor
- node -e "const a=require('@escape.tech/graphql-armor');const s=a.enableGraphQLArmor();console.log(Object.keys(s))"

### performance-debugging
Profile and fix N+1 queries, slow resolvers, and cache misses

**Commands:**
- `npx @apollo/server-plugin-response-cache --help || true`
- `node --trace-gc server.js 2>&1 | grep -i 'gc ' | head`
- `curl -s -X POST http://localhost:4001/graphql -H 'Content-Type: application/json' -d '{"query":"{ products { id name } }"}' -w '\n%{time_total}s'`
- `graphql-inspector audit docs/query.graphql schema.graphql`
- `npx apollo --version`

**Examples:**
- curl -s -X POST http://localhost:4001/graphql -H 'Content-Type: application/json' -d '{"query":"{ products { id name } }"}' -w '\n%{time_total}s'
- graphql-inspector audit docs/query.graphql schema.graphql
- node --trace-gc server.js 2>&1 | grep -i 'GC' | head -20
