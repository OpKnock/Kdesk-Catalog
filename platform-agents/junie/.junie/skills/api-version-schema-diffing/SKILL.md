---
name: "api-version-schema-diffing"
description: "Evolves GraphQL schemas safely: schema diffing with graphql-inspector, deprecation directives, coverage checks, and breaking-change detection. Use when working with schema diffing, deprecations or when the user mentions schema diffing, deprecations."
license: "MIT"
compatibility: "Requires node.js, python, openapi, postman. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Read Bash(curl:*) Grep Bash(npm:*) Bash(npx:*)"
---

Evolves GraphQL schemas safely: schema diffing with graphql-inspector, deprecation directives, coverage checks, and breaking-change detection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g @graphql-inspector/cli`, `curl -s -X POST http://localhost:4000/graphql -H 'Content-Ty`
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

**Parameters:**
- `old-schema` (string): Baseline schema file
- `new-schema` (string): Changed schema file
- `rule` (string): breaking, safe, or dangerous rules

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

## References
- [GraphQL Inspector](https://the-guild.dev/graphql/inspector/docs)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
