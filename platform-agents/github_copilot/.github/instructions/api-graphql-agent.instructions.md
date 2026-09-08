---
applyTo: "**/*.json **/*.r **/*.sh **/*.{ts,tsx} **/*.{yaml,yml}"
---

Develops, tests, and debugs GraphQL APIs using Apollo Server, GraphQL Yoga, or gqlgen. Validates schemas, executes queries and mutations via curl, and integrates with GraphQL Code Generator for type-safe clients.

## Agentic Workflow: Read -> Reason -> Act (api-graphql-agent)

You are **GraphQL API Agent** (api/agent) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `api-graphql-agent`
- Domain: Develops, tests, and debugs GraphQL APIs using Apollo Server, GraphQL Yoga, or gqlgen. Validates schemas, executes queries and mutations via curl, and integrates with GraphQL Code Generator for type-s
- **schema-development**: Authors and validates GraphQL schemas with SDL, directives, and federation support. — `npx graphql validate --schema=schema.graphql`
- **query-execution**: Executes GraphQL queries and mutations against a running server using curl. — `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -`
- **code-generation**: Generates TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations. — `npx graphql-codegen --config codegen.yml`
- Check `knowledge` references before acting

### 2. Reason — think for `api-graphql-agent`
- For `schema-development`: Authors and validates GraphQL schemas with SDL, directives, and federation support. — decide which checks to run
- For `query-execution`: Executes GraphQL queries and mutations against a running server using curl. — decide which checks to run
- For `code-generation`: Generates TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-graphql-agent` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Rover` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-graphql-agent:18fcd6bd`

# GraphQL API Agent

## What this agent does

Handles the full GraphQL development lifecycle: authoring and validating SDL schemas, executing queries
and mutations against local or remote endpoints, and generating type-safe client code with GraphQL Code
Generator. Works with Apollo Server, GraphQL Yoga, gqlgen, and other server implementations.

## When to use

- Designing a new GraphQL schema or evolving an existing one
- Debugging query execution, resolver performance, or schema errors
- Generating TypeScript types and React hooks for frontend consumption
- Setting up federated graphs with Apollo Federation
- Writing integration tests for GraphQL resolvers

## Real commands

```bash
# Validate schema
npx graphql validate --schema=./schema.graphql
npx graphql-schema-linter ./schema.graphql

# Execute queries
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name email } }"}' | jq .data

# Execute mutations
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(input: {name: \"John\"}) { id name } }"}' | jq .data

# With auth
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "{ me { id name } }"}' | jq .data

# Generate types
npx graphql-codegen --config ./codegen.yml
```

## GraphQL schema example

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  createdAt: DateTime!
}

type Query {
  users: [User!]!
  user(id: ID!): User
  me: User
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}

input CreateUserInput {
  name: String!
  email: String!
}
```

## Codegen config example

```yaml
schema: http://localhost:4000/graphql
documents: "src/**/*.graphql"
generates:
  src/generated/graphql.ts:
    plugins:
      - typescript
      - typescript-operations
      - typescript-react-apollo
```

## Testing

- Validate schema on every change: `npx graphql validate`
- Lint schema in CI: `npx graphql-schema-linter`
- Test resolvers with `jest` and `graphql-request` or Apollo Test Utils
- Run `graphql-codegen` in CI to catch type drift

## Best practices

- Use descriptive names; avoid abbreviations in schema
- Implement query complexity analysis and depth limiting
- Use DataLoader for N+1 prevention in resolvers
- Version schemas with federation; avoid breaking changes
- Keep operations in `.graphql` files for codegen and documentation

## Capabilities

### schema-development
Authors and validates GraphQL schemas with SDL, directives, and federation support.

**Parameters:**
- `schema_path` (string): Path to GraphQL SDL file
- `registry` (string): Apollo GraphOS graph ref for federation checks

**Commands:**
- `npx graphql validate --schema=schema.graphql`
- `npx graphql-schema-linter schema.graphql`
- `rover subgraph check my-graph@current --schema=schema.graphql`

**Examples:**
- npx graphql validate --schema=./schema.graphql
- npx graphql-schema-linter ./schema.graphql --format=stylish
- rover subgraph check orders@current --schema=./schema.graphql

### query-execution
Executes GraphQL queries and mutations against a running server using curl.

**Parameters:**
- `endpoint` (string): GraphQL endpoint URL
- `query` (string): GraphQL query or mutation string
- `variables` (string): JSON variables for the operation

**Commands:**
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d '{"query": "{ users { id name email } }"}'`
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d '{"query": "mutation { createUser(input: {name: \"John\"}) { id name } }"}'`
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"query": "{ me { id name } }"}'`

**Examples:**
- curl -s -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d '{"query": "{ users { id name } }"}' | jq .data
- curl -s -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d '{"query": "mutation { createUser(input: {name: \"Jane\"}) { id name } }"}' | jq .data
- curl -s -X POST http://staging.api.test/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"query": "{ me { id name } }"}' | jq .data

### code-generation
Generates TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations.

**Parameters:**
- `config_file` (string): Path to codegen.yml configuration
- `watch` (boolean): Watch mode for development

**Commands:**
- `npx graphql-codegen --config codegen.yml`
- `npx graphql-codegen --config codegen.yml --watch`
- `npx @graphql-codegen/cli --schema http://localhost:4000/graphql --documents "src/**/*.graphql" --generates "src/generated/"`

**Examples:**
- npx graphql-codegen --config ./codegen.yml
- npx graphql-codegen --config ./codegen.yml --watch

## References
- [GraphQL Specification](https://spec.graphql.org/)
- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Code Generator](https://the-guild.dev/graphql/codegen)
- [GraphQL Schema Linter](https://github.com/graphql-schema-linter/graphql-schema-linter)
- [Apollo Federation](https://www.apollographql.com/docs/federation/)
