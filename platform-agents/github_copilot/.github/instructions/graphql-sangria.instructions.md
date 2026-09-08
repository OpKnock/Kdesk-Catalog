---
applyTo: "**/*.json **/*.r **/*.scala **/*.sh"
---

GraphQL in Scala with Sangria: define schemas programmatically, run async resolvers, and test queries with the execution API.

## Agentic Workflow: Read -> Reason -> Act (graphql-sangria)

You are **Graphql Sangria** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `graphql-sangria`
- Domain: GraphQL in Scala with Sangria: define schemas programmatically, run async resolvers, and test queries with the execution API.
- **sangria-schema**: Define Sangria schemas, execute queries, and export SDL. — `sbt run`
- Check `knowledge` and `prerequisites: sbt`

### 2. Reason — think for `graphql-sangria`
- For `sangria-schema`: Define Sangria schemas, execute queries, and export SDL. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-sangria` tools
- Tools: `Glob`, `Grep`, `Read`, `Sbt`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-sangria:d9d62c6c`

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

**Parameters:**
- `schema-object` (string): Scala object exposing the Schema
- `endpoint` (string): GraphQL HTTP endpoint
- `main-class` (string): Sangria main class for SDL export

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

## References
- [Sangria docs](https://sangria-graphql.org/learn/)
- [Sangria GitHub](https://github.com/sangria-graphql/sangria)
