# Graphql

Authors GraphQL clients and tooling: queries, mutations, fragments, variables, and codegen with GraphQL Code Generator.

## Instructions

# GraphQL (Client)

Author GraphQL queries, mutations, and client tooling.

## When to Use

- Building frontend data layers against a GraphQL API
- Maintaining a typed client from the schema
- Validating queries before shipping them
- Using fragments to share field selections

## Query Example

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    name
    email
    posts(first: 5) {
      title
    }
  }
}
```

```json
{ "variables": { "id": "1" } }
```

## Commands

```bash
# Execute a query with variables
curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" \
  -d '{"query":"query($id: ID!){ user(id: $id) { name } }","variables":{"id":"1"}}'

# Codegen setup and run
npx @graphql-codegen/cli init
npx graphql-codegen --config codegen.yml
npx graphql-codegen --watch
```

## Codegen Config

```yaml
schema: http://localhost:4000/graphql
documents: "src/**/*.graphql"
generates:
  src/gql/generated.ts:
    plugins:
      - typescript
      - typescript-operations
      - typed-document-node
```

## Best Practices

- Use fragments for reusable field sets instead of repeating fields
- Always send variables rather than interpolating values into queries
- Enable codegen --watch in dev so types never drift
- Ship generated types and fail CI if generation is dirty
- Keep queries shallow unless depth is needed; watch complexity

## Capabilities

### graphql-client
Write and execute queries, mutations, and fragments.

**Commands:**
- `npx graphql-codegen`
- `npx graphql-query-complexity`
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d "{\"query\":\"query($id: ID!){ user(id: $id) { name } }\",\"variables\":{\"id\":\"1\"}}"`
- `npm install @apollo/client`

**Examples:**
- curl -X POST localhost:4000/graphql -d "{\"query\":\"mutation { addUser(name: \\\"Ann\\\") { id } }\"}"
- npx graphql-codegen --watch

### graphql-codegen
Generate TypeScript types and hooks from the schema.

**Commands:**
- `npx @graphql-codegen/cli init`
- `npx graphql-codegen --config codegen.yml`
- `npx graphql-codegen --watch`
- `npx graphql-tools load-documents "src/**/*.graphql"`

**Examples:**
- npx graphql-codegen --config codegen.ts
- npx graphql-codegen --dry-run
