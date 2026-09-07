---
trigger: glob
description: "General GraphQL development: introspect schemas, send queries and mutations with curl, and navigate SDL types from the command line. Use when working with graphql client, api or when the user mentions graphql client, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

General GraphQL development: introspect schemas, send queries and mutations with curl, and navigate SDL types from the command line.

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

# GraphQL

## What this skill does

GraphQL lets clients ask for exactly what they need in one round trip. This skill covers driving any GraphQL endpoint from the CLI: introspection, queries with variables, and mutations.

## When to use

- Exploring an unfamiliar GraphQL API
- Testing queries before writing client code
- Scripting data operations against a graph

## Real commands

```bash
# Root types
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { queryType { name } } }"}' | jq '.data'

# Fields of a type
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __type(name: \"Order\") { fields { name } } }"}' | jq '.data.__type.fields[].name'

# Query with variables
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"query($id: ID!){ order(id: $id) { id status } }","variables":{"id":"1"}}' | jq

# Mutation
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"mutation{ placeOrder(input: {amount: 42}) { orderId } }"}' | jq
```

## Response shape

```json
{
  "data": {"order": {"id": "1", "status": "paid"}},
  "errors": []
}
```

## Testing

```bash
# Confirm the endpoint is alive and the schema loads
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __typename }"}' | jq '.data.__typename'
```

## Best practices

- Always use variables, never string-interpolate values into queries.
- Request only the fields you use; no SELECT *.
- Handle errors[] explicitly; data may be partial.
- Use query names for tracing and logging.
- Introspect in dev, disable it in prod for security.

## Capabilities

### graphql-client
Introspect endpoints and run queries/mutations with curl and jq.

**Parameters:**
- `endpoint` (string): GraphQL HTTP endpoint
- `query` (string): GraphQL query or mutation document
- `variables` (object): Variables object for the query

**Commands:**
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { queryType { name } } }"}' | jq '.data'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __type(name: \"Order\") { fields { name type { kind ofType { name } } } } }"}' | jq '.data.__type.fields[].name'`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"query($id: ID!){ order(id: $id) { id status } }","variables":{"id":"1"}}' | jq`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"mutation{ placeOrder(input: {amount: 42}) { orderId } }"}' | jq`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types[].name' | head -20`

**Examples:**
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"query($id: ID!){ order(id: $id) { id status } }","variables":{"id":"1"}}' | jq
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __type(name: \"Order\") { fields { name } } }"}' | jq '.data.__type.fields[].name'
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"mutation{ placeOrder(input: {amount: 42}) { orderId } }"}' | jq

## References
- [GraphQL spec](https://spec.graphql.org/)
- [Introspection guide](https://graphql.org/learn/introspection/)
