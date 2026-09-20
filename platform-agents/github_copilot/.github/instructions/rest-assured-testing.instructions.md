---
applyTo: "**/*.java **/*.json **/*.kt **/*.r **/*.sh **/*.{yaml,yml}"
---

# rest-assured-testing

REST Assured Java API testing. Real REST Assured CLI.

## Instructions

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

**Commands:**
- `mvn test -Dtest=UsersApiTest`
- `./gradlew test --tests "com.example.UsersApiTest"`
- `mvn test -Dtest=UsersApiTest`
- `./gradlew test --tests "com.example.UsersApiTest"`

**Examples:**
- mvn test -Dtest=UsersApiTest
- ./gradlew test --tests "com.example.UsersApiTest"
- mvn test -Dtest=UsersApiTest
