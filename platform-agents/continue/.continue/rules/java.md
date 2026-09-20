---
name: "Java"
description: "Develops Java backend services with Maven/Gradle, Spring Boot, and the JVM toolchain including build, test, and packaging. Use when working with maven build, gradle build, backend or when the user mentions maven build, gradle build, backend."
globs: ["**/*.java", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Develops Java backend services with Maven/Gradle, Spring Boot, and the JVM toolchain including build, test, and packaging.

## Agentic Workflow: Read -> Reason -> Act (java)

You are **Java** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `java`
- Domain: Develops Java backend services with Maven/Gradle, Spring Boot, and the JVM toolchain including build, test, and packaging.
- **maven-build**: Build and test Maven projects. — `mvn clean package`
- **gradle-build**: Build and test Gradle projects. — `gradle build`
- Check `knowledge` and `prerequisites: gradle, mvn`

### 2. Reason — think for `java`
- For `maven-build`: Build and test Maven projects. — decide which checks to run
- For `gradle-build`: Build and test Gradle projects. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `java` tools
- Tools: `Glob`, `Grep`, `Read`, `Mvn`, `Gradle` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `java:495a33f8`

# Java

Backend services on the JVM with Maven or Gradle.

## When to Use

- Enterprise services with Spring Boot or Micronaut
- Long-lived services needing strong typing and tooling
- High-throughput apps where JVM GC tuning matters
- Teams already standardized on JVM tooling

## Maven Commands

```bash
mvn clean package
mvn test
mvn spring-boot:run
mvn dependency:tree
mvn install -DskipTests
mvn test -Dtest=OrderServiceTest
```

## Gradle Commands

```bash
gradle build
gradle test --tests "com.example.OrderTest"
gradle bootRun
gradle dependencies
gradle bootJar
```

## Spring Boot Example

```java
@RestController
public class HealthController {

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "ok");
    }
}
```

## Best Practices

- Pin JDK and build tool versions for reproducible builds
- Keep builds fast with -T (Gradle) or parallel modules
- Use dependency:tree / gradle dependencies to audit transitive deps
- Prefer records and sealed types for immutable DTOs
- Containerize with a multi-stage build; JRE base image is enough
- Enable failfast testing in CI with specific test filters

## Capabilities

### maven-build
Build and test Maven projects.

**Parameters:**
- `goal` (string): Maven goal to run
- `test` (string): Test filter

**Commands:**
- `mvn clean package`
- `mvn test`
- `mvn spring-boot:run`
- `mvn dependency:tree`
- `mvn install -DskipTests`

**Examples:**
- mvn clean package -DskipTests
- mvn test -Dtest=OrderServiceTest
- mvn versions:display-dependency-updates

### gradle-build
Build and test Gradle projects.

**Parameters:**
- `task` (string): Gradle task to run
- `test` (string): Test class filter

**Commands:**
- `gradle build`
- `gradle test`
- `gradle bootRun`
- `gradle dependencies`
- `gradle clean build`

**Examples:**
- gradle test --tests "com.example.OrderTest"
- gradle build -x test
- gradle bootJar

## References
- [Java SE Docs](https://docs.oracle.com/en/java/javase/)
- [Spring Boot Docs](https://docs.spring.io/spring-boot/)
- [Maven Docs](https://maven.apache.org/guides/)