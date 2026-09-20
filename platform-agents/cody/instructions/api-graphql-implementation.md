Implements GraphQL APIs: Apollo Server setup, resolver wiring, schema authoring, and playground-based testing.

## Agentic Workflow: Read -> Reason -> Act (api-graphql-implementation)

You are **Api Graphql Implementation** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-graphql-implementation`
- Domain: Implements GraphQL APIs: Apollo Server setup, resolver wiring, schema authoring, and playground-based testing.
- **server-implementation**: Stand up Apollo Server with resolvers and schema — `npm init -y && npm install @apollo/server graphql`
- **playground-testing**: Test queries and mutations via HTTP introspection — `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json`
- Check `knowledge` and `prerequisites: apollo-server, graphql-codegen, dataloader`

### 2. Reason — think for `api-graphql-implementation`
- For `server-implementation`: Stand up Apollo Server with resolvers and schema — decide which checks to run
- For `playground-testing`: Test queries and mutations via HTTP introspection — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-graphql-implementation` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-graphql-implementation:2c793017`

# API GraphQL (Implementation)

Builds working GraphQL APIs with Apollo Server.

## When to Use
- New GraphQL API for a service
- Migrating a simple REST endpoint
- Adding type safety to a backend

## Real Commands

```bash
# Bootstrap
npm init -y && npm install @apollo/server graphql

# Load schema files
npm install @graphql-tools/load-files @graphql-tools/schema

# Test via HTTP
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ products { id name } }"}'

# Introspect
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { queryType { name } } }"}'
```

## Schema First

```graphql
type Product { id: ID!, name: String!, price: Float }
type Query { products: [Product!]!, product(id: ID!): Product }
type Mutation { createProduct(name: String!): Product }
```

## Testing
Exercise queries, mutations, and error paths over HTTP.

## Best Practices
- Validate inputs in mutations
- Return nullable fields for optional data
- Enable Apollo Studio in production

## Capabilities

### server-implementation
Stand up Apollo Server with resolvers and schema

**Parameters:**
- `typeDefs` (string): SDL type definitions
- `resolvers` (string): Resolver map

**Commands:**
- `npm init -y && npm install @apollo/server graphql`
- `node -e "const {ApolloServer}=require('@apollo/server');console.log(typeof ApolloServer)"`
- `npm install @graphql-tools/load-files @graphql-tools/schema`
- `node -e "const {makeExecutableSchema}=require('@graphql-tools/schema');console.log(typeof makeExecutableSchema)"`
- `npm install graphql-tag`

**Examples:**
- npm init -y && npm install @apollo/server graphql
- npm install @graphql-tools/load-files @graphql-tools/schema
- node -e "const {makeExecutableSchema}=require('@graphql-tools/schema');console.log(typeof makeExecutableSchema)"

### playground-testing
Test queries and mutations via HTTP introspection

**Parameters:**
- `endpoint` (string): GraphQL endpoint URL
- `query` (string): GraphQL query string

**Commands:**
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { queryType { name } } }"}'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ products { id name } }"}'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"mutation { createProduct(name:\"x\") { id } }"}'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ products { id } }"}' -w '\n%{time_total}s'`
- `node -e "fetch('http://localhost:4000/graphql',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({query:'{ __typename }'})}).then(r=>r.json()).then(console.log)"`

**Examples:**
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ products { id name } }"}'
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { queryType { name } } }"}'
- node -e "fetch('http://localhost:4000/graphql',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({query:'{ __typename }'})}).then(r=>r.json()).then(console.log)"

## References
- [Apollo Server](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Tools](https://the-guild.dev/graphql/tools)
- [GraphQL Learn](https://graphql.org/learn/)
