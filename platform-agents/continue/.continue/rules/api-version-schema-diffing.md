---
name: "Api Version Schema Diffing"
description: "Evolves GraphQL schemas safely: schema diffing with graphql-inspector, deprecation directives, coverage checks, and breaking-change detection."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Api Version Schema Diffing

Evolves GraphQL schemas safely: schema diffing with graphql-inspector, deprecation directives, coverage checks, and breaking-change detection.

## Instructions

# API Version v2 - GraphQL

GraphQL schema evolution.

## What This Skill Does
- Detects breaking schema changes
- Manages deprecation directives
- Tracks field coverage

## When to Use
- Evolving GraphQL schemas safely
- Releasing schema changes
- Auditing unused fields

## Real Commands

```bash
npx @graphql-inspector/cli diff schema-old.graphql schema-new.graphql
npx @graphql-inspector/cli coverage --schema schema.graphql --queries "src/**/*.graphql"
```

## Deprecation Pattern

```graphql
type User {
  id: ID!
  legacyName: String @deprecated(reason: "Use displayName")
}
```

## Testing
- Diff every PR against the last release
- Fail CI on breaking diffs
- Remove deprecated fields after coverage drops


## Best Practices
- Prefer additive changes over breaks
- Use @deprecated before removal
- Track usage before deletion

## Capabilities

### schema-diffing
Diff GraphQL schemas for breaking changes

**Commands:**
- `npm install -g @graphql-inspector/cli`
- `npx @graphql-inspector/cli diff schema-old.graphql schema-new.graphql`
- `npx @graphql-inspector/cli diff --rule breaking schema-old.graphql schema-new.graphql`
- `npx @graphql-inspector/cli validate schema.graphql`
- `npx @graphql-inspector/cli coverage --schema schema.graphql --queries "src/**/*.graphql"`

**Examples:**
- diff reports breaking vs non-breaking changes
- --rule breaking filters to breaking-only
- coverage shows unused schema fields

### deprecations
Mark fields deprecated in the schema

**Commands:**
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __type(name: \"User\") { fields { name isDeprecated deprecationReason } } }"}' | jq '.data.__type.fields[0]'`
- `npx @graphql-inspector/cli diff schema.graphql schema-next.graphql --rule dangerous`
- `grep -c 'deprecated' schema.graphql`

**Examples:**
- -cli --help
- -api --help