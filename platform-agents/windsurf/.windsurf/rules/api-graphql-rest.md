---
trigger: glob
description: "Migrates and troubleshoots GraphQL: REST-to-GraphQL transitions, performance debugging, and breaking-change-safe schema evolution. Use when working with rest to graphql, schema evolution or when the user mentions rest to graphql, schema evolution."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Migrates and troubleshoots GraphQL: REST-to-GraphQL transitions, performance debugging, and breaking-change-safe schema evolution.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @graphql-tools/url-loader @graphql-tools/stitch`, `npx graphql-inspector diff schema-v1.graphql schema-v2.graph`
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

# API GraphQL (Migration & Evolution)

Migrates to GraphQL and keeps schemas evolving safely.

## When to Use
- REST-to-GraphQL migrations
- Schema breaking-change reviews
- Client compatibility concerns

## Real Commands

```bash
# Wrap REST during migration
curl -s http://localhost:3000/api/users | python -m json.tool
npm install @graphql-tools/url-loader

# Diff schemas
npx graphql-inspector diff schema-v1.graphql schema-v2.graphql

# Fail on removed fields
graphql-inspector diff schema-v1.graphql schema-v2.graphql --rule 'field.removed:error'

# Coverage of real queries
graphql-inspector coverage schema.graphql queries/**/*.graphql
```

## Evolution Rules
- Deprecate with @deprecated first
- Remove after a notice period
- Run diff checks in CI

## Testing
Run all client queries against the new schema before cutting over.

## Best Practices
- Keep the migration layer thin and temporary
- Track query coverage to avoid dead types

## Capabilities

### rest-to-graphql
Wrap REST endpoints with GraphQL resolvers during migration

**Parameters:**
- `restUrl` (string): REST endpoint to wrap
- `graphqlUrl` (string): GraphQL endpoint

**Commands:**
- `npm install @graphql-tools/url-loader @graphql-tools/stitch`
- `npm install graphql-http`
- `curl -s http://localhost:3000/api/users | python -m json.tool`
- `node -e "const {loadFromUrl}=require('@graphql-tools/url-loader');loadFromUrl('http://localhost:3000/graphql').then(s=>console.log(s?'schema loaded':'no'))"`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ users { id } }"}'`

**Examples:**
- curl -s http://localhost:3000/api/users | python -m json.tool
- node -e "const {loadFromUrl}=require('@graphql-tools/url-loader');loadFromUrl('http://localhost:3000/graphql').then(s=>console.log(s?'schema loaded':'no'))"
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ users { id } }"}'

### schema-evolution
Evolve schemas without breaking existing clients

**Parameters:**
- `oldSchema` (string): Old schema
- `newSchema` (string): New schema

**Commands:**
- `npx graphql-inspector diff schema-v1.graphql schema-v2.graphql`
- `graphql-inspector diff schema-v1.graphql schema-v2.graphql --rule 'field.removed:error'`
- `rover subgraph check mygraph@prod --name products --schema ./products.graphql`
- `node -e "console.log('deprecate before remove: @deprecated + notice period')"`
- `graphql-inspector coverage schema.graphql queries/**/*.graphql`

**Examples:**
- npx graphql-inspector diff schema-v1.graphql schema-v2.graphql
- rover subgraph check mygraph@prod --name products --schema ./products.graphql
- graphql-inspector coverage schema.graphql queries/**/*.graphql

## References
- [GraphQL Inspector Diff](https://the-guild.dev/graphql/inspector/docs/features/diff)
- [GraphQL Tools URL Loader](https://the-guild.dev/graphql/tools/docs/modules/url-loader)
