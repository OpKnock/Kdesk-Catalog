General Ktor development lifecycle: project scaffolding with the Ktor Gradle plugin, dependency management, and dev/test workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gradle wrapper --gradle-version 8.7`, `./gradlew build -x test`
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

# Ktor (General)

The full Ktor project lifecycle: scaffolding, building, running, and packaging.

## What this skill does

- Bootstraps Ktor projects with the Gradle plugin.
- Manages engines (Netty, CIO, Jetty) and plugins (content negotiation, auth).
- Builds runnable distributions.

## When to use

- Starting any Ktor server or client project.
- Upgrading Ktor versions and engines.
- Understanding which Ktor artifacts a project pulls in.

## Real commands

```bash
# Wrapper
gradle wrapper --gradle-version 8.7

# Full clean build (includes tests)
./gradlew clean build

# Dev run
./gradlew run

# Install distribution
./gradlew installDist
build/install/app/bin/app

# Inspect resolved dependencies
gradle dependencies --configuration runtimeClasspath | grep -i ktor
```

## build.gradle.kts example

```kotlin
plugins {
    kotlin("jvm") version "2.0.0"
    id("io.ktor.plugin") version "2.3.10"
}

application {
    mainClass.set("io.ktor.server.netty.EngineMain")
}

ktor {
    fatJar {
        archiveFileName.set("app-all.jar")
    }
}
```

## Testing

```bash
./gradlew test
```

## Best practices

- Pin Ktor and Kotlin versions; the plugin ties them together.
- Prefer EngineMain + application.conf for environment-driven config.
- Use the fatJar task for simple single-binary deploys.

## Capabilities

### ktor-lifecycle
Scaffold, build, and run Ktor projects with Gradle.

**Parameters:**
- `gradle_version` (string): Gradle wrapper version.
- `task` (string): Gradle task: run, build, clean, test.

**Commands:**
- `gradle wrapper --gradle-version 8.7`
- `./gradlew clean build`
- `./gradlew run`
- `gradle dependencies --configuration runtimeClasspath | grep -i ktor`

**Examples:**
- gradle wrapper --gradle-version 8.7
- ./gradlew clean build
- gradle dependencies --configuration runtimeClasspath | grep -i ktor

### plugin-config
Configure the Ktor Gradle plugin and application entry point.

**Parameters:**
- `main_class` (string): Application entry class, e.g. io.ktor.server.netty.EngineMain.

**Commands:**
- `./gradlew build -x test`
- `./gradlew installDist`
- `build/install/app/bin/app`
- `./gradlew dependencies --configuration ktor`

**Examples:**
- ./gradlew installDist
- build/install/app/bin/app
- ./gradlew build -x test

## References
- [Ktor Documentation](https://ktor.io/docs/welcome.html)
- [Ktor Gradle Plugin](https://ktor.io/docs/gradle-plugin.html)