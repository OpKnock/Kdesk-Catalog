---
trigger: glob
description: "REST Assured Java API testing. Real REST Assured CLI. Use when working with rest assured, testing or when the user mentions rest assured, testing."
globs: ["**/*.java", "**/*.json", "**/*.kt", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

REST Assured Java API testing. Real REST Assured CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn test -Dtest=UsersApiTest`
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

# REST Assured

REST Assured Java API testing using real CLI.

## When to Use

- Java API testing
- REST endpoint validation
- JSON/XML validation
- Schema validation

## Commands

```bash
# Run with Maven
mvn test -Dtest=UsersApiTest

# Run with Gradle
./gradlew test --tests "com.example.UsersApiTest"
```

## Dependencies

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <version>5.4.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>json-schema-validator</artifactId>
    <version>5.4.0</version>
    <scope>test</scope>
</dependency>
```

```kotlin
// build.gradle.kts
testImplementation("io.rest-assured:rest-assured:5.4.0")
testImplementation("io.rest-assured:json-schema-validator:5.4.0")
```

## Test

```java
// src/test/java/com/example/UsersApiTest.java
package com.example;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

class UsersApiTest {
    @BeforeEach
    void setUp() {
        RestAssured.baseURI = "https://api.example.com";
    }
    
    @Test
    void getUsers() {
        given()
            .when()
            .get("/users")
            .then()
            .statusCode(200)
            .body("size()", greaterThan(0));
    }
    
    @Test
    void createUser() {
        given()
            .contentType("application/json")
            .body("{\"name\": \"John\", \"email\": \"john@example.com\"}")
            .when()
            .post("/users")
            .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("name", equalTo("John"));
    }
    
    @Test
    void getUserById() {
        int id = given()
            .contentType("application/json")
            .body("{\"name\": \"Jane\", \"email\": \"jane@example.com\"}")
            .when()
            .post("/users")
            .then()
            .statusCode(201)
            .extract().path("id");
        
        given()
            .when()
            .get("/users/" + id)
            .then()
            .statusCode(200)
            .body("id", equalTo(id))
            .body("name", equalTo("Jane"));
    }
}
```

## Examples

```bash
# Run with Maven
mvn test -Dtest=UsersApiTest

# Run with Gradle
./gradlew test --tests "com.example.UsersApiTest"
```

## CI/CD

```yaml
# GitHub Actions
- name: Run REST Assured
  run: |
    mvn test -Dtest=UsersApiTest

# GitLab CI
rest-assured:
  stage: test
  script:
    - mvn test -Dtest=UsersApiTest
```

## Capabilities

### rest-assured
REST Assured Java API testing. Real REST Assured CLI.

**Parameters:**
- `tests` (string): CLI flag --tests observed in capability commands

**Commands:**
- `mvn test -Dtest=UsersApiTest`
- `./gradlew test --tests "com.example.UsersApiTest"`
- `mvn test -Dtest=UsersApiTest`
- `./gradlew test --tests "com.example.UsersApiTest"`

**Examples:**
- mvn test -Dtest=UsersApiTest
- ./gradlew test --tests "com.example.UsersApiTest"
- mvn test -Dtest=UsersApiTest

## References
- [rest-assured Skill Documentation](skills/testing/rest-assured.md)
