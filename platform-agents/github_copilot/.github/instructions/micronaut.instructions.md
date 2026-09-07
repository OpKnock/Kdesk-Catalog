---
applyTo: "**/*.java **/*.r **/*.sh **/*.sql **/*.{yaml,yml}"
---

Create and operate Micronaut applications: project scaffolding, HTTP endpoints, config, and the mn CLI lifecycle.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mn create-app com.example.app --features data-jpa,mysql,kafk`
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

# Micronaut

Micronaut is a modern JVM microservice framework with compile-time dependency injection and low startup memory.

## What this skill does

- Creates new Micronaut projects with the `mn` CLI
- Builds and runs them with Maven or Gradle
- Explains config-driven HTTP servers, health checks, and features

## When to use

- Greenfield JVM microservices where memory matters
- Moving from Spring Boot to a lighter runtime
- Generating GraalVM native images

## Real commands

```bash
# Create app with features
mn create-app com.example.app --features data-jpa,mysql,kafka

# Run via Maven wrapper
./mvnw mn:run

# Run tests
./mvnw test

# Health check
curl -s http://localhost:8080/health

# GraalVM native build
mn create-graal-app com.example.native --features graalvm
```

## application.yml

```yaml
micronaut:
  application:
    name: app
  server:
    port: 8080
```

## REST controller

```java
@Controller("/books")
public class BookController {
    @Get("/")
    public List<Book> list() { return repo.findAll(); }
}
```

## Best practices

- Use `mn create-app --features` to pull in only what you need
- Verify readiness via `/health` before routing traffic
- Keep config externalized in environment variables

## Capabilities

### micronaut-project
Scaffold, build, run and extend Micronaut projects using the mn CLI and build tools.

**Parameters:**
- `features` (array): Comma-separated Micronaut features to enable
- `package` (string): Base package for generated sources
- `build` (string): maven or gradle

**Commands:**
- `mn create-app com.example.app --features data-jpa,mysql,kafka`
- `mn create-graal-app com.example.native --features graalvm`
- `./mvnw mn:run`
- `./mvnw test`
- `curl -s http://localhost:8080/health`

**Examples:**
- mn create-app com.example.books --features data-jpa,mysql
- ./mvnw mn:run
- curl -s http://localhost:8080/health

## References
- [Micronaut Documentation](https://docs.micronaut.io/latest/guide/)
- [Micronaut Health Endpoints](https://micronaut-projects.github.io/micronaut-micrometer/latest/guide/)
