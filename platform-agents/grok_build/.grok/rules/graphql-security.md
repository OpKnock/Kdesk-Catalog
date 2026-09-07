GraphQL API security: test for introspection abuse, injection, and excessive depth; apply protections like query cost limits and allowlists.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -X POST http://localhost:4000/graphql -H 'Content-Ty`
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

# GraphQL Security

## What this skill does

GraphQL endpoints have unique attack surfaces: introspection leaks schemas, deep nested queries amplify cost, alias batching multiplies work, and batching fields can throttle-rate bypass. This skill probes and protects those.

## When to use

- Pre-launch security review of a GraphQL API
- Verifying protections after a change
- Incident triage on abusive queries

## Real commands

```bash
# Is introspection open?
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types | length'

# Alias batching probe (each alias is a separate field)
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ a: __typename b: __typename c: __typename }"}' | jq '.data | length'

# Automated scan
npx graphql-cop -t http://localhost:4000/graphql
```

## Protections example (Apollo Server)

```javascript
const { ApolloServerPluginLandingPageDisabled } = require('@apollo/server/plugin/landingPage/default')

// disable introspection in prod:
const server = new ApolloServer({
  introspection: process.env.NODE_ENV !== 'production',
  ...
})
```

## Depth/cost limiting (graphql-armor)

```javascript
import { EnvelopArmorPlugin } from '@envelop/armor'
// maxDepth: 6, maxAliases: 20, maxDirectives: 5
```

## Best practices

- Disable introspection in production (or gate it by role).
- Enforce depth and alias limits; GraphQL has no natural pagination guard.
- Rate limit per operation complexity, not per request.
- Use persisted query allowlists for critical endpoints.
- Never expose resolver internals in error messages.

## Capabilities

### graphql-security
Probe GraphQL endpoints for common vulnerabilities and validate protections.

**Parameters:**
- `endpoint` (string): GraphQL endpoint URL
- `query` (string): Probe query to send
- `protection` (string): introspection, depth-limit, cost-limit, allowlist

**Commands:**
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types | length'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __typename }"}' | jq '.errors'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ a: __typename b: __typename c: __typename }"}' | jq '.data | length'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"query{ user(id: \"1\") { id } }"}' | jq '.errors'`
- `npx graphql-cop -t http://localhost:4000/graphql`

**Examples:**
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types | length'
- npx graphql-cop -t http://localhost:4000/graphql
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ a: __typename b: __typename c: __typename }"}' | jq '.data | length'

## References
- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
- [graphql-cop](https://github.com/dolevf/graphql-cop)