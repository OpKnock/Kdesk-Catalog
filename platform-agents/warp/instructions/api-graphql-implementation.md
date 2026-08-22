# Api Graphql Implementation

Implements GraphQL APIs: Apollo Server setup, resolver wiring, schema authoring, and playground-based testing.

## Instructions

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
