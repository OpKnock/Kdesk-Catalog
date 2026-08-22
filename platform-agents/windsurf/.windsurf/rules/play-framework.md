---
trigger: glob
description: "Play Framework (Scala): sbt project setup, routes, controllers, and test/build lifecycle."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.scala", "**/*.sh"]
---

# Play Framework

Play Framework (Scala): sbt project setup, routes, controllers, and test/build lifecycle.

## Instructions

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
