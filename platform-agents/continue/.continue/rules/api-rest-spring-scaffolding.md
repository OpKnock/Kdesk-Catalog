---
name: "Api Rest Spring Scaffolding"
description: "Builds REST APIs with Spring Boot: Initializr scaffolding, Spring Web controllers, actuator health, and @Valid request validation. Use when working with spring scaffolding, spring web or when the user mentions spring scaffolding, spring web."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Builds REST APIs with Spring Boot: Initializr scaffolding, Spring Web controllers, actuator health, and @Valid request validation.

## Agentic Workflow: Read -> Reason -> Act (api-rest-spring-scaffolding)

You are **Api Rest Spring Scaffolding** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-rest-spring-scaffolding`
- Domain: Builds REST APIs with Spring Boot: Initializr scaffolding, Spring Web controllers, actuator health, and @Valid request validation.
- **spring-scaffolding**: Generate Spring Boot projects and run them — `curl -s https://start.spring.io/starter.zip -d dependencies=web,validation,data-`
- **spring-web**: Implement controllers with validation — `curl -s -X POST http://localhost:8080/api/users -H 'Content-Type: application/js`
- Check `knowledge` and `prerequisites: node.js, python, express, fastapi`

### 2. Reason — think for `api-rest-spring-scaffolding`
- For `spring-scaffolding`: Generate Spring Boot projects and run them — decide which checks to run
- For `spring-web`: Implement controllers with validation — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-rest-spring-scaffolding` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Unzip` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-rest-spring-scaffolding:225f38d7`

# API REST v3 - Spring Boot

REST APIs with Spring Boot.

## What This Skill Does
- Scaffolds Spring Boot projects from Initializr
- Implements REST controllers with validation
- Exposes actuator health endpoints

## When to Use
- Java enterprise REST services
- Teams standardized on Spring
- Services needing rich observability

## Real Commands

```bash
curl -s https://start.spring.io/starter.zip -d dependencies=web,validation,data-jpa,h2 -d type=maven-project -o demo.zip
unzip demo.zip -d demo && cd demo && ./mvnw spring-boot:run
curl -s http://localhost:8080/actuator/health | jq .status
```

## Controller Example

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @PostMapping
    public ResponseEntity<?> create(@Valid @RequestBody User user) {
        return ResponseEntity.created(URI.create("/api/users/1")).body(user);
    }
}
```

## Testing
- Assert actuator readiness before traffic
- Test validation failures return 400
- Use @WebMvcTest for controller slices

## Best Practices
- Use ProblemDetail for error responses
- Enable actuator security for production
- Keep DB migrations with Flyway

## Capabilities

### spring-scaffolding
Generate Spring Boot projects and run them

**Parameters:**
- `dependencies` (string): Comma-separated Spring starters
- `packageName` (string): Base Java package
- `build` (string): maven-project or gradle-project

**Commands:**
- `curl -s https://start.spring.io/starter.zip -d dependencies=web,validation,data-jpa,h2 -d type=maven-project -o demo.zip`
- `unzip demo.zip -d demo && cd demo && ./mvnw spring-boot:run`
- `curl -s http://localhost:8080/actuator/health | jq .status`
- `curl -s http://localhost:8080/actuator/health/readiness | jq .`

**Examples:**
- start.spring.io/starter.zip downloads a configured project
- GET /actuator/health reports liveness
- h2 dependency gives an in-memory database

### spring-web
Implement controllers with validation

**Commands:**
- `curl -s -X POST http://localhost:8080/api/users -H 'Content-Type: application/json' -d '{"name":"alice"}' -w '\n%{http_code}\n'`
- `curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:8080/api/users -H 'Content-Type: application/json' -d '{}'`
- `./mvnw clean test`

**Examples:**
- -cli --help
- -api --help

## References
- [Spring Initializr](https://start.spring.io/)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/reference/actuator/)