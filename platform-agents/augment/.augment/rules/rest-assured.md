---
type: agent_requested
description: "Expert Java REST API testing reference with Given/When/Then flows, JSONPath assertions, response validation, and Maven/Gradle integration."
---

# Rest Assured

Expert Java REST API testing reference with Given/When/Then flows, JSONPath assertions, response validation, and Maven/Gradle integration.

## Instructions

# Rest Assured

Expert skill for REST API testing in Java with Rest Assured.

## What this skill does

- Builds BDD-style tests: given() setup, when() request, then() assertions
- Asserts status codes, headers, and JSONPath expressions
- Runs individual tests via Maven or Gradle filters

## When to use

- Contract tests against Spring Boot or other Java APIs
- Smoke tests that should run in CI after deploy
- Local verification of endpoints during development

## Real commands

```bash
# Fetch the dependency explicitly
mvn dependency:get -Dartifact=io.rest-assured:rest-assured:5.4.0

# Run a whole test class
mvn test -Dtest=OrderApiTest

# Run a single method
mvn test -q -Dtest=OrderApiTest#shouldReturn201

# Gradle equivalent with verbose output
./gradlew test --tests '*ApiTest' --info
```

## Test example

```java
import static io.restassured.RestAssured.*;

given()
    .contentType("application/json")
    .body("{\"customer\":7,\"total\":199}")
.when()
    .post("/v1/orders")
.then()
    .statusCode(201)

    .body("id", greaterThan(0))
    .header("Location", not(emptyString()));

// JSONPath extraction

int id = when().get("/v1/orders").then().statusCode(200)
    .extract().path("data[0].id");
```

## Config example

```java
RestAssured.baseURI = "http://localhost:8080";
RestAssured.port = 8080;
```

## Testing

```bash
mvn test -Dtest=OrderApiTest
./gradlew test --tests '*ApiTest'
```

## Best practices

- Keep test data creation in @BeforeAll so tests stay independent
- Prefer JSONPath assertions over raw string contains checks
- Put integration tests behind a Maven profile so unit builds stay fast

## Capabilities

### rest-assured-bdd
Write and run BDD-style REST tests in Java with Rest Assured

**Commands:**
- `mvn dependency:get -Dartifact=io.rest-assured:rest-assured:5.4.0`
- `mvn test -Dtest=OrderApiTest`
- `mvn test -q -Dtest=OrderApiTest#shouldReturn201`
- `./gradlew test --tests '*ApiTest' --info`
- `mvn verify -Dskip.integration.tests=false`

**Examples:**
- mvn test -Dtest=OrderApiTest
- mvn test -q -Dtest=OrderApiTest#shouldReturn201
- ./gradlew test --tests '*ApiTest' --info