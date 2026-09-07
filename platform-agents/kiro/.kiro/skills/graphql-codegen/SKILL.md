---
name: "graphql-codegen"
description: "GraphQL Code Generator: generate TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations. Use when working with codegen, api or when the user mentions codegen, api."
license: "MIT"
compatibility: "Requires npx."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

GraphQL Code Generator: generate TypeScript types, React hooks, and client SDKs from GraphQL schemas and operations.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx graphql-codegen init`
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
