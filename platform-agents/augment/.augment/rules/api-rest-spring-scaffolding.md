---
type: agent_requested
description: "Builds REST APIs with Spring Boot: Initializr scaffolding, Spring Web controllers, actuator health, and @Valid request validation. Use when working with spring scaffolding, spring web or when the user mentions spring scaffolding, spring web."
---

Builds REST APIs with Spring Boot: Initializr scaffolding, Spring Web controllers, actuator health, and @Valid request validation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s https://start.spring.io/starter.zip -d dependencies=`, `curl -s -X POST http://localhost:8080/api/users -H 'Content-`
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