---
type: agent_requested
description: "http4s pure-functional HTTP in Scala: sbt project scaffolding, streaming routes, and running servers with curl verification. Use when working with http4s sbt, api or when the user mentions http4s sbt, api."
---

http4s pure-functional HTTP in Scala: sbt project scaffolding, streaming routes, and running servers with curl verification.

## Agentic Workflow: Read -> Reason -> Act (http4s)

You are **http4s** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `http4s`
- Domain: http4s pure-functional HTTP in Scala: sbt project scaffolding, streaming routes, and running servers with curl verification.
- **http4s-sbt**: Scaffold, build, and run http4s applications with sbt. — `sbt new http4s/http4s.g8 --name=http4s-quickstart`
- Check `knowledge` and `prerequisites: sbt`

### 2. Reason — think for `http4s`
- For `http4s-sbt`: Scaffold, build, and run http4s applications with sbt. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `http4s` tools
- Tools: `Glob`, `Grep`, `Read`, `Sbt`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `http4s:653bbea9`

# http4s

Pure-functional HTTP servers in Scala with http4s.

## What this skill does
47:   
- Scaffolds http4s projects with sbt.
- Writes effectful routes (IO, fs2 streams).
- Runs servers48:    with Ember and verifies with curl.
- Tests routes without starting a listener.

## When to use
49:   
- A Scala service needs a typed, functional HTTP layer.
- Streaming responses (SSE, file uploads)50:    fit fs2 well.
- Teams coming from cats-effect want end-to-end FP.

## Real commands

```bash
51:   # Scaffold
sbt new http4s/http4s.g8 --name=http4s-quickstart
cd http4s-quickstart

# Run
sbt run
52:   # or with a custom port
sbt "run --port 9090"

# Test
sbt test

# Verify
curl -s -X POST http://localhost:8080/hello/World
53:   ```

## Route example

```scala
import org.http4s.*
import org.http4s.dsl.io.*

val routes =54:    HttpRoutes.of[IO] {
  case GET -> Root =>
    Ok("Hello, http4s!")
  case req @ POST -> Root55:    / "hello" / name =>
    Ok(s"Hello, $name")
}
```

## Server

```scala
import org.http4s.ember.server.EmberServerBuilder
56:   import com.comcast.ip4s.*

EmberServerBuilder
  .default[IO]
  .withHost(ipv4"0.0.0.0")
  .withPort(port"57:   8080")
  .withHttpApp(routes.orNotFound)
  .build
  .use(_ => IO.never)
  .unsafeRunSync()
```
58:   
## Testing

```bash
curl -s http://localhost:8080/
sbt test
```

## Best practices

- Keep59:    routes pure: return F[_] responses, never block.
- Use http4s-dsl matchers for typed path extraction.
60:   - Prefer Ember for new projects; blaze for legacy needs.
- Test with the `http4s-laws`/munit-supertest61:    style rather than booting a server.

## Example exchange

```
User: Serve JSON from an http4s62:    route.
Agent: Use the json4s/circe entity encoder:
       case GET -> Root / "health" => Ok(Map("63:   status" -> "ok").asJson)
```

## Capabilities

### http4s-sbt
Scaffold, build, and run http4s applications with sbt.

**Parameters:**
- `port` (integer): Server port, default 8080.
- `scala_version` (string): Scala version for the build (e.g. 2.13 or 3).
- `project_name` (string): Project name from the giter8 template.

**Commands:**
- `sbt new http4s/http4s.g8 --name=http4s-quickstart`
- `sbt run`
- `sbt test`
- `curl -s -X POST http://localhost:8080/hello/World`
- `sbt "runMain com.example.quickstart.Server"`

**Examples:**
- sbt new http4s/http4s.g8 --name=api
- sbt "run --port 9090"
- curl -s http://localhost:8080/

## References
- [http4s Docs](https://http4s.org/)
- [http4s Quickstart](https://http4s.org/docs/quickstart/)