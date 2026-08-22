---
type: agent_requested
description: "Implements versioning in Java/Spring Boot: versioned controllers, request mapping constraints, media-type versioning, and endpoint tests."
---

# api-versioning-engineer

Implements versioning in Java/Spring Boot: versioned controllers, request mapping constraints, media-type versioning, and endpoint tests.

## Instructions

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