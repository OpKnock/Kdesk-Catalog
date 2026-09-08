---
name: "graphql-schema-designer"
description: "Designs and evolves GraphQL schemas: linting with graphql-schema-linter, drift checks with graphql-inspector, and typed codegen. Use when working with lint, diff or when the user mentions lint, diff."
license: "MIT"
compatibility: "Requires apollo-server, graphql-codegen, rover, altair, postman, graphql-inspector."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

Designs and evolves GraphQL schemas: linting with graphql-schema-linter, drift checks with graphql-inspector, and typed codegen.

## Agentic Workflow: Read -> Reason -> Act (graphql-schema-designer)

You are **graphql-schema-designer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `graphql-schema-designer`
- Domain: Designs and evolves GraphQL schemas: linting with graphql-schema-linter, drift checks with graphql-inspector, and typed codegen.
- **lint**: Lint GraphQL schemas against rulesets. — `npx graphql-schema-linter schema.graphql`
- **diff**: Compare schema versions and generate typed clients. — `npx graphql-inspector diff old.graphql new.graphql`
- Check `knowledge` and `prerequisites: apollo-server, graphql-codegen, rover, altair`

### 2. Reason — think for `graphql-schema-designer`
- For `lint`: Lint GraphQL schemas against rulesets. — decide which checks to run
- For `diff`: Compare schema versions and generate typed clients. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-schema-designer` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-schema-designer:6105d60a`

# GraphQL Schema Design

Design clean GraphQL schemas and keep them stable across releases.

## When to Use

- Designing a new GraphQL API surface
- Reviewing schema changes in pull requests
- Generating typed clients for consumers

## Schema linting

```graphql
"""A product in the catalog"""
type Product implements Node {
  """Globally unique id"""
  id: ID!
  """Display name"""
  name: String!
  """Price in cents"""
  price: Int!
}
```

```bash
npx graphql-schema-linter schema.graphql --rules fields-have-descriptions,types-have-descriptions
```

## Breaking change detection

```bash
npx graphql-inspector diff schema-prod.graphql schema-next.graphql
```

Breaking = field removed, type made non-null, arg added without default. Fix them before merge.

## Operation validation

```bash
npx graphql-inspector validate --schema schema.graphql 'operations/**/*.graphql'
```

## Codegen

```ts
// codegen.ts
import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  schema: 'schema.graphql',
  documents: 'operations/**/*.graphql',
  generates: {
    'src/gql/': {
      preset: 'client',
      plugins: []
    }
  }
};
export default config;
```

```bash
npx graphql-codegen --config codegen.ts
```

## Best practices

- Use interfaces and unions over flag enums where behavior differs.
- Keep enums sorted; reordering is a breaking change.
- Prefer nullable return fields over throwing for optional data.
- Name arguments explicitly; never rely on positional order.

## Testing

Run the linter and inspector diff in CI on every PR touching schema files.

## Capabilities

### lint
Lint GraphQL schemas against rulesets.

**Parameters:**
- `rules` (string): Comma-separated rule names
- `format` (string): stylish or json output
- `ignore` (string): Rules to skip

**Commands:**
- `npx graphql-schema-linter schema.graphql`
- `npx graphql-schema-linter schema.graphql --rules fields-have-descriptions,types-have-descriptions`
- `npx graphql-schema-linter schema.graphql --format json`
- `npx graphql-schema-linter 'schema/**/*.graphql' --ignore 'deprecations-have-a-reason'`
- `npx graphql-schema-linter schema.graphql --comment-descriptions`

**Examples:**
- npx graphql-schema-linter schema.graphql --rules enum-values-sorted-alphabetically
- npx graphql-schema-linter 'schema/**/*.graphql' --format json > lint.json
- npx graphql-schema-linter schema.graphql --ignore 'description-style'

### diff
Compare schema versions and generate typed clients.

**Parameters:**
- `schema` (string): Schema file(s) to analyze
- `config` (string): codegen configuration file
- `watch` (string): Regenerate on file changes

**Commands:**
- `npx graphql-inspector diff old.graphql new.graphql`
- `npx graphql-inspector validate --schema new.graphql 'operations/**/*.graphql'`
- `npx graphql-inspector similar --schema schema.graphql`
- `npx graphql-codegen --config codegen.ts`
- `npx graphql-codegen generate --config codegen.ts --watch`

**Examples:**
- npx graphql-inspector diff schema-2026-07.graphql schema-2026-08.graphql
- npx graphql-codegen --config codegen.ts --silent
- npx graphql-inspector validate --schema schema.graphql 'src/**/*.graphql'

## References
- [GraphQL Schema Spec](https://graphql.org/learn/schema/)
- [GraphQL Inspector](https://the-guild.dev/graphql/inspector/docs)
- [GraphQL Codegen](https://the-guild.dev/graphql/codegen/docs)
