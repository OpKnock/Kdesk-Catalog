---
type: agent_requested
description: "Migrates and troubleshoots GraphQL: REST-to-GraphQL transitions, performance debugging, and breaking-change-safe schema evolution."
---

# Api Graphql Rest

Migrates and troubleshoots GraphQL: REST-to-GraphQL transitions, performance debugging, and breaking-change-safe schema evolution.

## Instructions

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