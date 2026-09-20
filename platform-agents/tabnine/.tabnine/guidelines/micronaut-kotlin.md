Build Micronaut applications with the Kotlin language: scaffolding, controllers, coroutines, and Gradle/Kotlin DSL setup.

## Agentic Workflow: Read -> Reason -> Act (micronaut-kotlin)

You are **Micronaut Kotlin** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `micronaut-kotlin`
- Domain: Build Micronaut applications with the Kotlin language: scaffolding, controllers, coroutines, and Gradle/Kotlin DSL setup.
- **micronaut-kotlin-scaffold**: Scaffold Kotlin Micronaut apps and services with the Micronaut CLI and manage the build. — `mn create-app com.example.demo --lang kotlin --build gradle`
- Check `knowledge` and `prerequisites: ./gradlew`

### 2. Reason — think for `micronaut-kotlin`
- For `micronaut-kotlin-scaffold`: Scaffold Kotlin Micronaut apps and services with the Micronaut CLI and manage the build. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `micronaut-kotlin` tools
- Tools: `Glob`, `Grep`, `Read`, `Mn`, `./gradlew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `micronaut-kotlin:15b728f6`

# Micronaut Kotlin

Micronaut with Kotlin gives compile-time dependency injection and first-class coroutines support.

## What this skill does

- Scaffolds Kotlin Micronaut projects (Gradle or Maven)
- Adds controllers, services and clients in Kotlin
- Uses kapt/ksp for compile-time DI processing

## When to use

- Starting a new Kotlin JVM microservice
- Adding coroutine-based endpoints to an existing Micronaut app
- Configuring Kotlin-specific features (kotlinx.serialization, ksp)

## Real commands

```bash
# Create Kotlin app with Gradle
mn create-app com.example.demo --lang kotlin --build gradle

# Add a controller
mn create-controller com.example.HelloController --lang kotlin

# Run and test
./gradlew run
./gradlew test

# CLI application (picocli)
mn create-cli-app cli-app --lang kotlin
```

## Coroutines controller

```kotlin
@Controller("/hello")
class HelloController {
    @Get("/") 
    suspend fun hello(): String = coroutineScope { "Hello from Kotlin" }
}
```

## build.gradle.kts essentials

```kotlin
plugins {
    id("org.jetbrains.kotlin.jvm") version "1.9.22"
    id("io.micronaut.library") version "4.2.1"
}
```

## Best practices

- Prefer KSP over kapt (`mn create-app --features kotlin,ksp`)
- Use `suspend` functions for non-blocking endpoints
- Test with `./gradlew test` and MicronautTest annotation

## Capabilities

### micronaut-kotlin-scaffold
Scaffold Kotlin Micronaut apps and services with the Micronaut CLI and manage the build.

**Parameters:**
- `lang` (string): kotlin (with kapt or ksp) or java
- `features` (array): Micronaut features to include, e.g. kapt, data-jpa, kafka
- `build` (string): gradle or maven

**Commands:**
- `mn create-app com.example.demo --lang kotlin --build gradle`
- `mn create-controller com.example.HelloController --lang kotlin`
- `./gradlew run`
- `./gradlew test`
- `mn create-cli-app cli-app --lang kotlin`

**Examples:**
- mn create-app com.example.orders --lang kotlin --features kapt
- ./gradlew run
- ./gradlew test --tests com.example.HelloControllerTest

## References
- [Micronaut Kotlin Guide](https://docs.micronaut.io/latest/guide/index.html)
- [Micronaut CLI](https://micronaut-projects.github.io/micronaut-starter/latest/guide/)