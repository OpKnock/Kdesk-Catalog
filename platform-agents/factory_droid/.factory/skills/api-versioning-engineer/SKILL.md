---
name: "api-versioning-engineer"
description: "Implements versioning in Java/Spring Boot: versioned controllers, request mapping constraints, media-type versioning, and endpoint tests. Use when working with spring versioning, version tests or when the user mentions spring versioning, version tests."
license: "MIT"
compatibility: "Requires node.js, python, openapi-generator, postman, stoplight-studio. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(./mvnw:*) Bash(curl:*)"
---

Implements versioning in Java/Spring Boot: versioned controllers, request mapping constraints, media-type versioning, and endpoint tests.

## Agentic Workflow: Read -> Reason -> Act (api-versioning-engineer)

You are **api-versioning-engineer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-versioning-engineer`
- Domain: Implements versioning in Java/Spring Boot: versioned controllers, request mapping constraints, media-type versioning, and endpoint tests.
- **spring-versioning**: Version Spring REST controllers — `curl -s https://start.spring.io/starter.zip -d dependencies=web,validation -d pa`
- **version-tests**: Test versioned endpoints — `./mvnw test -Dtest=UserControllerTest`
- Check `knowledge` and `prerequisites: node.js, python, openapi-generator`

### 2. Reason — think for `api-versioning-engineer`
- For `spring-versioning`: Version Spring REST controllers — decide which checks to run
- For `version-tests`: Test versioned endpoints — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-versioning-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `./mvnw` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-versioning-engineer:39352cd6`

# API Versioning Engineer

Spring Boot API versioning.

## What This Skill Does
- Versions endpoints with media types
- Controls content negotiation
- Tests version selection

## When to Use
- Java/Spring APIs with external clients
- Media-type versioning strategies
- Backward-compatible evolution

## Real Commands

```bash
curl -s -H 'Accept: application/vnd.example.v1+json' http://localhost:8080/api/users | jq '.version'
curl -s -H 'Accept: application/vnd.example.v2+json' http://localhost:8080/api/users | jq '.version'
```

## Controller Example

```java
@RestController
@RequestMapping(value = "/api/users", produces = "application/vnd.example.v2+json")
public class UserV2Controller { }
```

## Testing
- Test each version media type
- Verify Vary header includes Accept
- Confirm 406 for unsupported versions


## Best Practices
- Register media types explicitly
- Document versions in OpenAPI
- Keep version-specific logic separated

## Capabilities

### spring-versioning
Version Spring REST controllers

**Parameters:**
- `media-type` (string): Vendor media type
- `version` (string): Version in the media type
- `endpoint` (string): Controller endpoint

**Commands:**
- `curl -s https://start.spring.io/starter.zip -d dependencies=web,validation -d packageName=com.example -o ver.zip && unzip -o ver.zip -d ver`
- `curl -s -H 'Accept: application/vnd.example.v1+json' http://localhost:8080/api/users | jq '.version'`
- `curl -s -H 'Accept: application/vnd.example.v2+json' http://localhost:8080/api/users | jq '.version'`
- `./mvnw clean test`
- `./mvnw spring-boot:run`

**Examples:**
- produces/consumes media types version routes
- Accept: application/vnd.example.v2+json selects v2
- Controller-level @RequestMapping versioning

### version-tests
Test versioned endpoints

**Commands:**
- `./mvnw test -Dtest=UserControllerTest`
- `curl -s -D- -H 'Accept: application/vnd.example.v1+json' http://localhost:8080/api/users | grep -i '^vary:'`
- `curl -s -H 'Accept: application/json' http://localhost:8080/api/users -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help

## References
- [Spring MVC Media Types](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping-media-types.html)
- [Spring Boot Docs](https://docs.spring.io/spring-boot/index.html)
