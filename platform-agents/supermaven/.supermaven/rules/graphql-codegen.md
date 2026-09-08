GraphQL Code Generator: generate TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations.

## Agentic Workflow: Read -> Reason -> Act (graphql-codegen)

You are **Graphql Codegen** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `graphql-codegen`
- Domain: GraphQL Code Generator: generate TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations.
- **codegen**: Generate typed code from GraphQL schemas and operation documents. — `npx graphql-codegen init`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `graphql-codegen`
- For `codegen`: Generate typed code from GraphQL schemas and operation documents. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-codegen` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-codegen:74ae3a2b`

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

**Parameters:**
- `config-file` (string): codegen.yml path
- `schema` (string): Schema source: URL or .graphql file
- `documents` (string): Glob of operation documents

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

## References
- [GraphQL Code Generator docs](https://the-guild.dev/graphql/codegen/docs)
- [codegen.yml reference](https://the-guild.dev/graphql/codegen/docs/config-reference/codegen-config)