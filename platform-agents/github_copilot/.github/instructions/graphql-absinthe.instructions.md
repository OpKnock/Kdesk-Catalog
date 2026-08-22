---
applyTo: "**/*.json **/*.r **/*.sh"
---

# Graphql Absinthe

GraphQL on Elixir with Absinthe: scaffold schemas, run the mix compiler, generate docs, and test GraphQL queries.

## Instructions

# GraphQL Absinthe

## What this skill does

Absinthe is the GraphQL implementation for Elixir. Schemas are defined with the `use Absinthe.Schema` macro, resolvers handle fields, and mix tasks export the schema as SDL/JSON for tooling.

## When to use

- Building GraphQL APIs on Phoenix/Elixir
- Exporting the schema for client codegen
- Testing resolvers in isolation

## Real commands

```bash
# Export schema as SDL/JSON
mix absinthe.schema.sdl --schema MyApp.Schema > schema.graphql
mix absinthe.schema.json --schema MyApp.Schema > schema.json

# Tests
mix test test/graphql

# Interactive
iex -S mix phx.server
```

## Schema example

```elixir
defmodule MyApp.Schema do
  use Absinthe.Schema

  import_types Absinthe.Type.Custom

  query do
    field :order, :order do
      arg :id, non_null(:id)
      resolve fn %{id: id}, _ ->
        case Orders.get(id) do
          nil -> {:error, "not found"}
          order -> {:ok, order}
        end
      end
    end
  end

  object :order do
    field :id, non_null(:id)
    field :status, non_null(:string)
  end
end
```

## Testing

```elixir
# Absinthe test helper: run a query against the schema directly
Absinthe.run(~s({ order(id: "1") { id status } }), MyApp.Schema)
```

## Best practices

- Keep resolvers in context modules, not inline in the schema.
- Use `Absinthe.Test` for schema-level tests without HTTP.
- Export the SDL in CI and diff it to catch schema drift.
- Use dataloader for batched associations.
- Document fields with `@doc` strings; they surface in schema tooling.

## Capabilities

### absinthe-development
Manage Absinthe schemas, compile, and run queries in a Phoenix/IEx context.

**Commands:**
- `mix deps.get && mix absinthe.schema.json --schema MyApp.Schema > schema.json`
- `mix absinthe.schema.sdl --schema MyApp.Schema > schema.graphql`
- `mix test test/graphql`
- `mix run -e "IO.inspect(MyApp.Schema)"`
- `iex -S mix phx.server`

**Examples:**
- mix absinthe.schema.sdl --schema MyApp.Schema > schema.graphql
- mix test test/graphql
- mix absinthe.schema.json --schema MyApp.Schema > schema.json && jq '.data.__schema.queryType.name' schema.json
