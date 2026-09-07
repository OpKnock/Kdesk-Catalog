---
trigger: glob
description: "Quarkus with Kotlin: quarkus CLI scaffolding, Kotlin endpoints, coroutines and native builds. Use when working with quarkus kotlin build, api or when the user mentions quarkus kotlin build, api."
globs: ["**/*.kt", "**/*.r", "**/*.sh"]
---

Quarkus with Kotlin: quarkus CLI scaffolding, Kotlin endpoints, coroutines and native builds.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `quarkus create app my-app --lang kotlin`
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

**Parameters:**
- `lang` (string): kotlin or java
- `extensions` (array): Quarkus extensions to add
- `package_type` (string): uber-jar, fast-jar or native

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

## References
- [Quarkus Kotlin Guide](https://quarkus.io/guides/kotlin)
- [Quarkus CLI Reference](https://quarkus.io/guides/cli-tooling)
