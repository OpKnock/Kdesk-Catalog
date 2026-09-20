---
name: "graphql-sangria"
description: "GraphQL in Scala with Sangria: define schemas programmatically, run async resolvers, and test queries with the execution API."
---

# Graphql Sangria

GraphQL in Scala with Sangria: define schemas programmatically, run async resolvers, and test queries with the execution API.

## Instructions

# GraphQL Sangria

## What this skill does

Sangria is a Scala GraphQL library with a powerful programmatic schema DSL. Resolvers return Futures for async sources; `Executor.execute` runs queries and `SchemaRenderer` exports SDL.

## When to use

- Scala/Akka services adding GraphQL
- Teams that prefer explicit schema DSLs over macros
- Type-safe async resolvers with Future/Task

## Real commands

```bash
# Build and test with sbt
sbt compile
sbt test

# Run the server
sbt run

# Query it
curl -s -X POST http://localhost:8080/graphql -H 'Content-Type: application/json' -d '{"query":"{ characters { name } }"}' | jq

# Export SDL
sbt 'runMain example.SchemaExport'
```

## Schema example

```scala
import sangria.schema._
import sangria.execution.Executor

val Character = ObjectType(
  "Character",
  "A character in the story",
  fields[MyCtx, Character](Field("name", StringType, resolve = _.value.name))
)

val Query = ObjectType("Query", fields[MyCtx, Unit](
  Field("characters", ListType(Character), resolve = ctx => repo.all(ctx.ctx))
))

val schema = Schema(Query)
```

## Executing a query

```scala
import scala.concurrent.Await
import scala.concurrent.duration._

val result = Await.result(Executor.execute(schema, query), 10.seconds)
println(result)
```

## Best practices

- Use `FieldTags` and middleware for auth, not resolver checks.
- Keep the context (MyCtx) for DI of repos and caches.
- Export SDL from CI to catch breaking changes.
- Use deferred resolution (Deferred/Projector) for N+1 batching.
- Keep schema construction lazy or cached; it is expensive.

## Capabilities

### sangria-schema
Define Sangria schemas, execute queries, and export SDL.

**Commands:**
- `sbt run`
- `sbt compile`
- `sbt test`
- `curl -s -X POST http://localhost:8080/graphql -H 'Content-Type: application/json' -d '{"query":"{ characters { name } }"}' | jq`
- `sbt 'runMain example.SchemaExport'`

**Examples:**
- sbt compile && sbt test
- curl -s -X POST http://localhost:8080/graphql -H 'Content-Type: application/json' -d '{"query":"{ characters { name } }"}' | jq
- sbt 'runMain example.SchemaExport'
