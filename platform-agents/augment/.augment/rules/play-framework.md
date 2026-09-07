---
type: agent_requested
description: "Play Framework (Scala): sbt project setup, routes, controllers, and test/build lifecycle. Use when working with play scala workflow, api or when the user mentions play scala workflow, api."
---

Play Framework (Scala): sbt project setup, routes, controllers, and test/build lifecycle.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `sbt new playframework/play-scala-seed.g8`
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

# Play Framework

Play is a reactive web framework for Scala and Java with hot reloading and type-safe routes.

## What this skill does

- Scaffolds projects from giter8 seeds
- Defines routes and controllers
- Runs tests and builds distributions

## When to use

- Scala HTTP services
- Teams already on the JVM

## Real commands

```bash
# New project
sbt new playframework/play-scala-seed.g8

# Run with hot reload
sbt run
sbt run -Dhttp.port=9001

# Test / build
sbt test
sbt compile
sbt dist
```

## Routes (conf/routes)

```scala
GET     /users              controllers.UserController.list
GET     /users/:id          controllers.UserController.show(id: Long)
POST    /users              controllers.UserController.create
```

## Controller

```scala
class UserController @Inject()(cc: ControllerComponents) extends AbstractController(cc) {
  def list = Action { Ok(Json.toJson(List("alice", "bob"))) }
}
```

## Best practices

- Keep routes type-safe with path params
- Write tests with PlaySpecification + ScalaTest
- Use `sbt dist` for production zips

## Capabilities

### play-scala-workflow
Scaffold Play Framework apps with sbt, add routes/controllers, and run the test-build cycle.

**Parameters:**
- `port` (integer): HTTP port for sbt run
- `seed` (string): giter8 seed template name
- `sbt_task` (string): sbt task: compile, test, dist, run

**Commands:**
- `sbt new playframework/play-scala-seed.g8`
- `sbt run`
- `sbt test`
- `sbt compile`
- `sbt dist`

**Examples:**
- sbt run -Dhttp.port=9001
- sbt test
- sbt dist

## References
- [Play Framework Docs](https://www.playframework.com/documentation/latest/Home)
- [play-scala-seed template](https://github.com/playframework/play-scala-seed.g8)