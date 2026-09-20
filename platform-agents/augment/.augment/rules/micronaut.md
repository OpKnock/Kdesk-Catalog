---
type: agent_requested
description: "Create and operate Micronaut applications: project scaffolding, HTTP endpoints, config, and the mn CLI lifecycle."
---

# Micronaut

Create and operate Micronaut applications: project scaffolding, HTTP endpoints, config, and the mn CLI lifecycle.

## Instructions

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