---
applyTo: "**/*.json **/*.r **/*.sh"
---

Deep GraphQL expertise: query planning, cost analysis, persisted queries, caching, and advanced security hardening.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install graphql-cost-analysis`, `npx @apollo/server-plugin-response-cache --help || true`
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

**Parameters:**
- `maxCost` (string): Maximum query cost
- `maxDepth` (string): Maximum query depth

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

**Parameters:**
- `query` (string): GraphQL query to benchmark
- `endpoint` (string): GraphQL endpoint URL

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

## References
- [GraphQL Armor](https://escape.tech/blog/graphql-armor/)
- [Apollo Server Docs](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Inspector](https://the-guild.dev/graphql/inspector/docs)
