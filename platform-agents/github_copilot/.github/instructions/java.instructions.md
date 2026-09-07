---
applyTo: "**/*.java **/*.r **/*.sh"
---

Develops Java backend services with Maven/Gradle, Spring Boot, and the JVM toolchain including build, test, and packaging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn clean package`, `gradle build`
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
