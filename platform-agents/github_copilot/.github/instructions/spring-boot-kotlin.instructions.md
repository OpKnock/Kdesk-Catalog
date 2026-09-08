---
applyTo: "**/*.java **/*.kt **/*.r **/*.sh **/*.{yaml,yml}"
---

Scaffolds, runs, and tests Spring Boot applications written in Kotlin with Gradle. Generates projects from start.spring.io with selected starters, runs via bootRun, probes actuator health endpoints, and executes Kotlin test classes.

## Agentic Workflow: Read -> Reason -> Act (spring-boot-kotlin)

You are **Spring Boot Kotlin** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `spring-boot-kotlin`
- Domain: Scaffolds, runs, and tests Spring Boot applications written in Kotlin with Gradle. Generates projects from start.spring.io with selected starters, runs via bootRun, probes actuator health endpoints, a
- **spring-kotlin-workflow**: Scaffolds, runs, and tests Spring Boot applications written in Kotlin with Gradle. Generates project — `curl -s https://start.spring.io/starter.zip -d language=kotlin -d type=gradle-pr`
- Check `knowledge` and `prerequisites: ./gradlew`

### 2. Reason — think for `spring-boot-kotlin`
- For `spring-kotlin-workflow`: Scaffolds, runs, and tests Spring Boot applications written in Kotlin with Gradle. Generates projects from start.spring. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `spring-boot-kotlin` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `./gradlew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `spring-boot-kotlin:3940d053`

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
