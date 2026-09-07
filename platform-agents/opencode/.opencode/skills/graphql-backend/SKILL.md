---
name: "graphql-backend"
description: "Authors GraphQL clients and tooling: queries, mutations, fragments, variables, and codegen with GraphQL Code Generator. Use when working with graphql client, graphql codegen, backend or when the user mentions graphql client, graphql codegen, backend."
---

Authors GraphQL clients and tooling: queries, mutations, fragments, variables, and codegen with GraphQL Code Generator.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx graphql-codegen`, `npx @graphql-codegen/cli init`
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
