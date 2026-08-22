---
name: "graphql-codegen"
description: "GraphQL Code Generator: generate TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations."
type: knowledge
triggers: ["graphql-codegen", "codegen"]
---

# Graphql Codegen

GraphQL Code Generator: generate TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations.

## Instructions

# GraphQL Codegen

## What this skill does

GraphQL Code Generator turns schemas + operations into typed code: TypeScript types, React hooks, Zod schemas, or full SDKs. It validates queries against the schema at generation time.

## When to use

- Eliminating handwritten API types in clients
- Catching stale operations against a changed schema
- Generating hooks for React/Apollo or SWR

## Real commands

```bash
# Interactive setup
npx graphql-codegen init

# One-shot generation
npx graphql-codegen --config codegen.yml

# Watch mode during development
npx graphql-codegen --watch --config codegen.yml

# CI gate: fail if types are stale
npx graphql-codegen --check --config codegen.yml
```

## codegen.yml example

```yaml
schema: http://localhost:4000/graphql
documents: './src/**/*.graphql'
generates:
  ./src/__generated__/graphql.ts:
    plugins:
      - typescript
      - typescript-operations
      - typescript-react-apollo
    config:
      withHooks: true
```

## Testing

```bash
# Run against a local schema and verify output types
npx graphql-codegen --config codegen.yml && grep -c 'export type' src/__generated__/graphql.ts
```

## Best practices

- Commit generated files or regenerate in CI; never both silently.
- Use `--check` in CI to fail on drift.
- Keep documents colocated with components (*.graphql next to tsx).
- Point the schema at a CI-published artifact, not a dev server.
- Add a custom plugin only when built-in types are insufficient.

## Capabilities

### codegen
Generate typed code from GraphQL schemas and operation documents.

**Commands:**
- `npx graphql-codegen init`
- `npx graphql-codegen --config codegen.yml`
- `npx graphql-codegen --watch --config codegen.yml`
- `npx graphql-codegen --config codegen.yml --verbose`
- `npx graphql-codegen --check --config codegen.yml`

**Examples:**
- npx graphql-codegen init && npx graphql-codegen --config codegen.yml
- npx graphql-codegen --config codegen.yml
- npx graphql-codegen --check --config codegen.yml
