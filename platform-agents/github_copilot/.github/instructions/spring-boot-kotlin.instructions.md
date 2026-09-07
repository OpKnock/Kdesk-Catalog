---
applyTo: "**/*.java **/*.kt **/*.r **/*.sh **/*.{yaml,yml}"
---

Scaffolds, runs, and tests Spring Boot applications written in Kotlin with Gradle. Generates projects from start.spring.io with selected starters, runs via bootRun, probes actuator health endpoints, and executes Kotlin test classes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s https://start.spring.io/starter.zip -d language=kotl`
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

# Spring Boot with Kotlin

Hand-crafted skill for Spring Boot applications written in Kotlin.

## What this skill does

- Generates a Kotlin + Gradle project from start.spring.io
- Runs the app with bootRun and checks actuator health
- Runs Kotlin test classes and builds the jar

## When to use

- Starting a new Kotlin service on Spring Boot
- Verifying a generated project boots before writing code
- Running the suite in CI with Gradle

## Real commands

```bash
# Scaffold: Kotlin + Gradle + web/data-jpa/actuator
curl -s https://start.spring.io/starter.zip -d language=kotlin -d type=gradle-project -d dependencies=web,data-jpa,actuator -o demo.zip && unzip demo.zip

# Run the app
./gradlew bootRun

# Health check
curl -s localhost:8080/actuator/health | jq .status

# Run tests
./gradlew test --tests 'com.example.demo.DemoApplicationTests'

# Build and run the jar
./gradlew build && java -jar build/libs/demo-0.0.1-SNAPSHOT.jar
```

## Controller example

```kotlin
package com.example.demo

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class HelloController {
    @GetMapping("/hello")
    fun hello() = mapOf("message" to "Hello from Kotlin")
}
```

## Testing

```bash
./gradlew bootRun &
curl -s localhost:8080/hello | jq .message
curl -s localhost:8080/actuator/health | jq .status
./gradlew test
```

## Best practices

- Keep controller code in Kotlin but services testable via interfaces
- Use application.yaml for per-environment profiles
- Let Gradle handle the Spring plugin version via the wrapper

## Capabilities

### spring-kotlin-workflow
Scaffolds, runs, and tests Spring Boot applications written in Kotlin with Gradle. Generates projects from start.spring.io with selected starters, runs via bootRun, probes actuator health endpoints, and executes Kotlin test classes.

**Parameters:**
- `dependencies` (string): Comma-separated Spring Boot starters (e.g., web,data-jpa,actuator)
- `test_class` (string): Fully qualified test class name
- `java_version` (integer): Java version for the project (e.g., 17, 21)

**Commands:**
- `curl -s https://start.spring.io/starter.zip -d language=kotlin -d type=gradle-project -d dependencies=web,data-jpa,actuator -o demo.zip`
- `./gradlew bootRun`
- `curl -s localhost:8080/actuator/health`
- `./gradlew test --tests 'com.example.demo.DemoApplicationTests'`
- `./gradlew build`
- `java -jar build/libs/demo-0.0.1-SNAPSHOT.jar`

**Examples:**
- curl -s https://start.spring.io/starter.zip -d language=kotlin -d type=gradle-project -d dependencies=web,data-jpa,actuator -o demo.zip
- ./gradlew bootRun
- curl -s localhost:8080/actuator/health
- ./gradlew test --tests 'com.example.demo.DemoApplicationTests'
- ./gradlew build && java -jar build/libs/demo-0.0.1-SNAPSHOT.jar

## References
- [Spring Boot docs](https://docs.spring.io/spring-boot/index.html)
