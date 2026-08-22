---
name: "vertx"
description: "Builds reactive APIs with Eclipse Vert.x on the JVM. Scaffolds Maven projects via the official archetype, runs verticles with hot reload, packages executable fat jars, and verifies endpoints with curl."
---

# Vertx

Builds reactive APIs with Eclipse Vert.x on the JVM. Scaffolds Maven projects via the official archetype, runs verticles with hot reload, packages executable fat jars, and verifies endpoints with curl.

## Instructions

# Vert.x

## What this skill does

Build reactive, event-loop-driven APIs with Eclipse Vert.x on the JVM. Covers scaffolding via the official Maven archetype, development mode with hot redeploy, packaging executable fat jars, and verifying endpoints.

## When to use

- Building high-throughput async APIs in Java/Kotlin
- Prototyping with Vert.x Web Router
- Packaging services for deployment

## Real commands

```bash
# Scaffold a new project
mvn archetype:generate \
  -DarchetypeGroupId=io.vertx \
  -DarchetypeArtifactId=vertx-maven-archetype \
  -DarchetypeVersion=4.5.10

# Development mode with hot reload
mvn compile vertx:run

# Run a specific verticle
mvn compile vertx:run -Dvertx.id=main-verticle

# Package the fat jar
mvn clean package -DskipTests

# Run the packaged jar
java -jar target/hello-1.0.0-fat.jar

# Verify the endpoint
curl -s http://localhost:8080/hello
```

## Minimal MainVerticle.java

```java
public class MainVerticle extends AbstractVerticle {
  @Override
  public void start(Promise<Void> startPromise) {
    vertx.createHttpServer()
      .requestHandler(req -> req.response()
        .putHeader("content-type", "application/json")
        .end("{\"status\":\"ok\"}"))
      .listen(8080, http -> {
        if (http.succeeded()) startPromise.complete();
        else startPromise.fail(http.cause());
      });
  }
}
```

## Best practices

- Never block the event loop; use `vertx.executeBlocking` for JDBC calls
- Use Vert.x Web Router with sub-routers per resource
- Prefer the service proxy pattern for inter-verticle calls
- Pin the archetype version in CI builds

## Testing

```bash
mvn compile vertx:run &
sleep 8
curl -s http://localhost:8080/hello -w '\n%{http_code}\n'
```

## Capabilities

### vertx-project
Scaffold, run, and package Vert.x applications

**Commands:**
- `mvn archetype:generate -DarchetypeGroupId=io.vertx -DarchetypeArtifactId=vertx-maven-archetype -DarchetypeVersion=4.5.10`
- `mvn compile vertx:run`
- `mvn package`
- `java -jar target/hello-1.0.0-fat.jar`
- `curl -s http://localhost:8080/hello`

**Examples:**
- mvn compile vertx:run -Dvertx.id=main-verticle
- mvn clean package -DskipTests
- curl -s http://localhost:8080/api/tasks | jq ".length"
