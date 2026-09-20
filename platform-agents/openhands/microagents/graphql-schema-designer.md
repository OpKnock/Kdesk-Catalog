---
name: "graphql-schema-designer"
description: "Designs and evolves GraphQL schemas: linting with graphql-schema-linter, drift checks with graphql-inspector, and typed codegen."
type: knowledge
triggers: ["graphql-schema-designer", "lint", "diff"]
---

# graphql-schema-designer

Designs and evolves GraphQL schemas: linting with graphql-schema-linter, drift checks with graphql-inspector, and typed codegen.

## Instructions

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
