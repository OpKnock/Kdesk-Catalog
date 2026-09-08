---
trigger: glob
description: "Create and operate Micronaut applications: project scaffolding, HTTP endpoints, config, and the mn CLI lifecycle. Use when working with micronaut project, api or when the user mentions micronaut project, api."
globs: ["**/*.java", "**/*.r", "**/*.sh", "**/*.sql", "**/*.{yaml,yml}"]
---

Create and operate Micronaut applications: project scaffolding, HTTP endpoints, config, and the mn CLI lifecycle.

## Agentic Workflow: Read -> Reason -> Act (micronaut)

You are **Micronaut** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `micronaut`
- Domain: Create and operate Micronaut applications: project scaffolding, HTTP endpoints, config, and the mn CLI lifecycle.
- **micronaut-project**: Scaffold, build, run and extend Micronaut projects using the mn CLI and build tools. — `mn create-app com.example.app --features data-jpa,mysql,kafka`
- Check `knowledge` and `prerequisites: ./mvnw`

### 2. Reason — think for `micronaut`
- For `micronaut-project`: Scaffold, build, run and extend Micronaut projects using the mn CLI and build tools. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `micronaut` tools
- Tools: `Glob`, `Grep`, `Read`, `Mn`, `./mvnw` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `micronaut:3b42eb19`

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
