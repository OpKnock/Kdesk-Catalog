---
name: "Graphql Gqlgen"
description: "GraphQL in Go with gqlgen: generate resolvers from SDL, run the server, and iterate on schema-driven development."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Graphql Gqlgen

GraphQL in Go with gqlgen: generate resolvers from SDL, run the server, and iterate on schema-driven development.

## Instructions

# GraphQL gqlgen

## What this skill does

gqlgen is a schema-first GraphQL server library for Go: it generates all boilerplate from your SDL, leaving you to implement resolver functions with strong types.

## When to use

- Building typed GraphQL services in Go
- Schema-first teams that want generated code, not mux glue
- High-performance Go backends

## Real commands

```bash
# Scaffold the project
 go run github.com/99designs/gqlgen init

# Generate after schema changes
 go run github.com/99designs/gqlgen generate

# Regenerate with a custom config
 go run github.com/99designs/gqlgen --config gqlgen.yml

# Run and test
 go run ./server.go
 go test ./... -v
```

## gqlgen.yml example

```yaml
schema:
  - schema.graphql
resolver:
  layout: follow-schema
  dir: graph
  package: graph
autobind:
  - "github.com/example/orders/graph/model"
```

## Resolver stub example

```go
func (r *queryResolver) Order(ctx context.Context, id string) (*model.Order, error) {
	o, err := r.OrdersRepo.Get(ctx, id)
	if errors.Is(err, storage.ErrNotFound) {
		return nil, fmt.Errorf("order %s not found", id)
	}
	return o, err
}
```

## Testing

```bash
# Hit the generated playground endpoint
curl -s -X POST http://localhost:8080/query -H 'Content-Type: application/json' -d '{"query":"{ order(id: \"1\") { id } }"}' | jq
```

## Best practices

- Keep the SDL as the source of truth; never hand-edit generated files.
- Re-run generate in CI and fail on git diff.
- Autobind model types to avoid duplicate model structs.
- Implement resolvers in a separate layer (repos/services).
- Use gqlgen plugins sparingly; stock generators cover most needs.

## Capabilities

### gqlgen-codegen
Generate Go resolver code from GraphQL SDL and run the server.

**Commands:**
- `go run github.com/99designs/gqlgen init`
- `go run github.com/99designs/gqlgen generate`
- `go run github.com/99designs/gqlgen --config gqlgen.yml`
- `go run ./server.go`
- `go test ./... -v`

**Examples:**
- go run github.com/99designs/gqlgen init && go run github.com/99designs/gqlgen generate
- go run ./server.go
- go run github.com/99designs/gqlgen generate && go test ./... -v