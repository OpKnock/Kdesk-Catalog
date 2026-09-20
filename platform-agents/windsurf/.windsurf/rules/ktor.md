---
trigger: glob
description: "General Ktor development lifecycle: project scaffolding with the Ktor Gradle plugin, dependency management, and dev/test workflows. Use when working with ktor lifecycle, plugin config, api or when the user mentions ktor lifecycle, plugin config, api."
globs: ["**/*.go", "**/*.kt", "**/*.r", "**/*.sh"]
---

General Ktor development lifecycle: project scaffolding with the Ktor Gradle plugin, dependency management, and dev/test workflows.

## Agentic Workflow: Read -> Reason -> Act (ktor)

You are **Ktor** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `ktor`
- Domain: General Ktor development lifecycle: project scaffolding with the Ktor Gradle plugin, dependency management, and dev/test workflows.
- **ktor-lifecycle**: Scaffold, build, and run Ktor projects with Gradle. — `gradle wrapper --gradle-version 8.7`
- **plugin-config**: Configure the Ktor Gradle plugin and application entry point. — `./gradlew build -x test`
- Check `knowledge` and `prerequisites: ./gradlew, build/install/app/bin/app, gradle`

### 2. Reason — think for `ktor`
- For `ktor-lifecycle`: Scaffold, build, and run Ktor projects with Gradle. — decide which checks to run
- For `plugin-config`: Configure the Ktor Gradle plugin and application entry point. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ktor` tools
- Tools: `Glob`, `Grep`, `Read`, `Gradle`, `./gradlew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ktor:da22c0b1`

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
