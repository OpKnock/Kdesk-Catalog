---
type: agent_requested
description: "Quarkus with Kotlin: quarkus CLI scaffolding, Kotlin endpoints, coroutines and native builds."
---

# Quarkus Kotlin

Quarkus with Kotlin: quarkus CLI scaffolding, Kotlin endpoints, coroutines and native builds.

## Instructions

# Quarkus Kotlin

Quarkus brings fast startup and low memory to Kotlin microservices.

## What this skill does

- Scaffolds Kotlin projects with the quarkus CLI
- Adds extensions and Kotlin endpoints
- Builds native images

## When to use

- Kotlin JVM services needing GraalVM native
- Replacing heavier frameworks

## Real commands

```bash
# Create with Kotlin
quarkus create app my-app --lang kotlin

# Dev mode with hot reload
quarkus dev

# Add extensions
quarkus ext add rest
quarkus ext add rest-client,resteasy-reactive-jackson

# Build
quarkus build
quarkus build -Dquarkus.package.type=uber-jar
./mvnw compile
```

## Kotlin endpoint

```kotlin
@Path("/hello")
class HelloResource {
    @GET
    suspend fun hello(): String = "Hello from Kotlin"
}
```

## Native build

```bash
quarkus build --native
```

## Best practices

- Use suspend functions with RESTEasy Reactive
- Test with quarkus dev and the continuous test mode
- Profile with `quarkus dev` before native builds

## Capabilities

### quarkus-kotlin-build
Create Kotlin Quarkus apps, add extensions and run the dev loop with the quarkus CLI.

**Commands:**
- `quarkus create app my-app --lang kotlin`
- `quarkus dev`
- `quarkus build`
- `quarkus ext add rest`
- `./mvnw compile`

**Examples:**
- quarkus create app orders --lang kotlin -P io.quarkus.platform:quarkus-bom:3.10.0
- quarkus dev
- quarkus build -Dquarkus.package.type=uber-jar