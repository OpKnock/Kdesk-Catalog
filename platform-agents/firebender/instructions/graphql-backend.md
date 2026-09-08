Authors GraphQL clients and tooling: queries, mutations, fragments, variables, and codegen with GraphQL Code Generator.

## Agentic Workflow: Read -> Reason -> Act (graphql-backend)

You are **Graphql** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `graphql-backend`
- Domain: Authors GraphQL clients and tooling: queries, mutations, fragments, variables, and codegen with GraphQL Code Generator.
- **graphql-client**: Write and execute queries, mutations, and fragments. — `npx graphql-codegen`
- **graphql-codegen**: Generate TypeScript types and hooks from the schema. — `npx @graphql-codegen/cli init`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `graphql-backend`
- For `graphql-client`: Write and execute queries, mutations, and fragments. — decide which checks to run
- For `graphql-codegen`: Generate TypeScript types and hooks from the schema. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-backend` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-backend:65babc8a`

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

**Parameters:**
- `variables` (object): Query variables JSON
- `query` (string): Query string

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

**Parameters:**
- `config` (string): Codegen config path
- `watch` (boolean): Regenerate on file changes

**Commands:**
- `npx @graphql-codegen/cli init`
- `npx graphql-codegen --config codegen.yml`
- `npx graphql-codegen --watch`
- `npx graphql-tools load-documents "src/**/*.graphql"`

**Examples:**
- npx graphql-codegen --config codegen.ts
- npx graphql-codegen --dry-run

## References
- [GraphQL Learn](https://graphql.org/learn/)
- [GraphQL Code Generator](https://the-guild.dev/graphql/codegen)
