# Graphql Schema Tooling

GraphQL schema quality tooling: lint SDL with graphql-schema-linter, detect breaking changes with graphql-inspector, and validate operations against schemas.

## Instructions

# GraphQL v2

## What this skill does

Schema quality tooling keeps GraphQL APIs maintainable: linters enforce naming/description rules, inspectors diff schemas for breaking changes, and validators check client operations against the schema.

## When to use

- Enforcing schema conventions in CI
- Reviewing a PR that changes the schema
- Catching operations that would break before deploy

## Real commands

```bash
# Lint with rule selection
npx graphql-schema-linter schema.graphql --rules=fields-have-descriptions,types-have-descriptions

# Machine-readable lint output
npx graphql-schema-linter --format json schema.graphql > lint.json

# Breaking change diff
npx graphql-inspector diff schema-old.graphql schema-new.graphql | jq

# Validate client operations
npx graphql-inspector validate schema.graphql 'src/**/*.graphql'

# Capture the live schema
npx graphql-inspector introspect http://localhost:4000/graphql --write schema.graphql
```

## .graphql-schema-linter.yml example

```yaml
rules:
  - fields-have-descriptions
  - types-have-descriptions
  - no-hashtag-description
  - relay-page-info-spec
```

## CI gate example

```bash
npx graphql-schema-linter schema.graphql && \
  npx graphql-inspector diff schema-main.graphql schema-pr.graphql --rule breaking | grep -q . && exit 1 || echo 'no breaking changes'
```

## Testing

```bash
# Confirm lint config catches a planted violation
echo 'type Bad{field:String}' > /tmp/bad.graphql && npx graphql-schema-linter /tmp/bad.graphql --rules=types-have-descriptions; echo "exit=$?"
```

## Best practices

- Run the linter on every schema commit.
- Gate merges on breaking change diffs; use @deprecated instead of removals.
- Validate all client documents in CI against the prod schema.
- Commit the schema SDL and diff it against live introspection.
- Keep descriptions on public types; they become the docs.

## Capabilities

### schema-tooling
Lint schemas, diff versions for breaking changes, and validate operations.

**Commands:**
- `npx graphql-schema-linter schema.graphql --rules=fields-have-descriptions,types-have-descriptions`
- `npx graphql-schema-linter --format json schema.graphql > lint.json`
- `npx graphql-inspector diff schema-old.graphql schema-new.graphql | jq`
- `npx graphql-inspector validate schema.graphql 'src/**/*.graphql'`
- `npx graphql-inspector introspect http://localhost:4000/graphql --write schema.graphql`

**Examples:**
- npx graphql-schema-linter schema.graphql --rules=fields-have-descriptions,types-have-descriptions
- npx graphql-inspector diff schema-old.graphql schema-new.graphql | jq
- npx graphql-inspector validate schema.graphql 'src/**/*.graphql'
