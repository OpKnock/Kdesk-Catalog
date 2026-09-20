---
applyTo: "**/*.java **/*.r **/*.sh **/*.{yaml,yml}"
---

Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, runs in dev mode with spring-boot:run, probes actuator endpoints, packages executable JARs, and runs filtered test suites.

## Agentic Workflow: Read -> Reason -> Act (spring-boot)

You are **Spring Boot** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `spring-boot`
- Domain: Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, runs in dev mode with spring-boot:run, probes actuator endpoints, packages executable JARs, and runs 
- **spring-boot-lifecycle**: Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, r — `curl -s https://start.spring.io/starter.zip -d type=maven-project -d dependencie`
- Check `knowledge` and `prerequisites: ./mvnw`

### 2. Reason — think for `spring-boot`
- For `spring-boot-lifecycle`: Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, runs in dev mode with — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `spring-boot` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `./mvnw` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `spring-boot:610a31e2`

# Spring Boot

Hand-crafted skill for the Spring Boot application lifecycle with Maven.

## What this skill does

- Generates Maven projects from start.spring.io with selected starters
- Runs the app in dev mode and probes actuator endpoints
- Packages an executable jar and runs the test suite

## When to use

- Starting or onboarding a Spring Boot service
- Local development loop: run, hit actuator, iterate
- Building a release artifact for deployment

## Real commands

```bash
# Scaffold a Maven project with web + actuator on Java 21
curl -s https://start.spring.io/starter.zip -d type=maven-project -d dependencies=web,actuator -d javaVersion=21 -o demo.zip && unzip -q demo.zip -d demo

# Dev run
./mvnw spring-boot:run

# Actuator health
curl -s localhost:8080/actuator/health

# Tests
./mvnw test
./mvnw test -Dtest=HelloControllerTest

# Package and run the jar
./mvnw package -DskipTests && java -jar target/demo-0.0.1-SNAPSHOT.jar
```

## application.yaml

```yaml
server:
  port: 8080
spring:
  application:
    name: demo
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
```

## Testing

```bash
./mvnw spring-boot:run &
curl -s localhost:8080/actuator/health | jq .status
./mvnw test
```

## Best practices

- Use the mvnw wrapper so builds are reproducible
- Expose only safe actuator endpoints in production
- Prefer the packaged jar over spring-boot:run in prod

## Capabilities

### spring-boot-lifecycle
Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, runs in dev mode with spring-boot:run, probes actuator endpoints, packages executable JARs, and runs filtered test suites.

**Parameters:**
- `java_version` (integer): Java version for the project (e.g., 17, 21)
- `dependencies` (string): Comma-separated Spring Boot starters (e.g., web,actuator,data-jpa)
- `test_class` (string): Specific test class to run

**Commands:**
- `curl -s https://start.spring.io/starter.zip -d type=maven-project -d dependencies=web,actuator -d javaVersion=21 -o demo.zip`
- `./mvnw spring-boot:run`
- `curl -s localhost:8080/actuator/health`
- `./mvnw test`
- `./mvnw test -Dtest=HelloControllerTest`
- `./mvnw package -DskipTests`
- `java -jar target/demo-0.0.1-SNAPSHOT.jar`

**Examples:**
- curl -s https://start.spring.io/starter.zip -d type=maven-project -d dependencies=web,actuator -d javaVersion=21 -o demo.zip
- ./mvnw spring-boot:run
- curl -s localhost:8080/actuator/health
- ./mvnw test
- ./mvnw package -DskipTests && java -jar target/demo-0.0.1-SNAPSHOT.jar

## References
- [Spring Boot reference](https://docs.spring.io/spring-boot/index.html)
