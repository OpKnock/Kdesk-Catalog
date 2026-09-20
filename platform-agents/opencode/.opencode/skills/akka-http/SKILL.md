---
name: "akka-http"
description: "Builds streaming, reactive HTTP services in Scala with Akka HTTP: route DSL, JSON marshalling, TestKit testing, and sbt workflows. Use when working with project scaffold, test and build, api or when the user mentions project scaffold, test and build, api."
---

Builds streaming, reactive HTTP services in Scala with Akka HTTP: route DSL, JSON marshalling, TestKit testing, and sbt workflows.

## Agentic Workflow: Read -> Reason -> Act (akka-http)

You are **Akka Http** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `akka-http`
- Domain: Builds streaming, reactive HTTP services in Scala with Akka HTTP: route DSL, JSON marshalling, TestKit testing, and sbt workflows.
- **project-scaffold**: Create an Akka HTTP project from the giter8 template and manage deps. — `sbt new akka/akka-http-quickstart-scala.g8`
- **test-and-build**: Test routes with akka-http-testkit, package, and run in CI. — `sbt test`
- Check `knowledge` and `prerequisites: java, sbt`

### 2. Reason — think for `akka-http`
- For `project-scaffold`: Create an Akka HTTP project from the giter8 template and manage deps. — decide which checks to run
- For `test-and-build`: Test routes with akka-http-testkit, package, and run in CI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `akka-http` tools
- Tools: `Glob`, `Grep`, `Read`, `Sbt`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `akka-http:a20e74cf`

# Akka HTTP

## What this skill does

Creates reactive HTTP services in Scala with Akka HTTP: bootstrapping via giter8, route DSL composition, JSON marshalling of case classes, TestKit testing, and sbt-assembly packaging.

## When to use

- A streaming, backpressure-aware REST API in Scala
- Adding WebSockets or SSE to an actor system
- Refactoring a Play app into lighter Akka HTTP routes

## Real commands

```bash
sbt new akka/akka-http-quickstart-scala.g8 --name=my-api

sbt compile
sbt run
curl http://localhost:8080/hello?name=world

sbt test
sbt "testOnly com.acme.UserRouteSpec"

sbt assembly
java -jar target/scala-2.13/my-api-assembly-0.1.0.jar
```

## Route example

```scala
import akka.http.scaladsl.server.Directives._

val route =
  pathPrefix("api") {
    get {
      path("users" / LongNumber) { id =>
        complete(s"user $id")
      }
    }
  }
```

## Testing

- Use akka-http-testkit + scalatest: `Post("/users") ~> route ~> check`
- Assert status and JSON with responseAs[String] or a marshaller

## Best practices

- Put routes in traits that can be mixed into tests
- Use typed marshalling instead of raw strings
- Pin Akka versions in build.sbt
- Prefer pipelining/backlog tuning on the HttpServer for production

## Capabilities

### project-scaffold
Create an Akka HTTP project from the giter8 template and manage deps.

**Parameters:**
- `name` (string): Project name for the giter8 template
- `port` (number): Port for the HTTP server binding

**Commands:**
- `sbt new akka/akka-http-quickstart-scala.g8`
- `sbt update`
- `sbt compile`
- `sbt run`
- `curl http://localhost:8080/hello`

**Examples:**
- sbt new akka/akka-http-quickstart-scala.g8 --name=my-api
- sbt "runMain com.acme.Main 8080"
- curl http://localhost:8080/hello?name=world

### test-and-build
Test routes with akka-http-testkit, package, and run in CI.

**Parameters:**
- `test_filter` (string): Test name pattern for testOnly
- `assembly_output` (string): Path to the fat jar

**Commands:**
- `sbt test`
- `sbt "testOnly com.acme.RouteSpec"`
- `sbt assembly`
- `sbt clean test assembly`
- `java -jar target/scala-2.13/my-api-assembly-0.1.0.jar`

**Examples:**
- sbt test
- sbt assembly && java -jar target/scala-2.13/my-api-assembly-0.1.0.jar
- sbt "testOnly *HealthSpec*"

## References
- [Akka HTTP Docs](https://doc.akka.io/docs/akka-http/current/)
- [Akka HTTP TestKit](https://doc.akka.io/docs/akka-http/current/routing-dsl/testkit.html)
- [Akka Quickstart](https://doc.akka.io/docs/akka-http/current/introduction.html)
