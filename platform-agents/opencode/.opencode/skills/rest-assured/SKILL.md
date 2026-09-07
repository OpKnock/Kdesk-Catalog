---
name: "rest-assured"
description: "Expert Java REST API testing reference with Given/When/Then flows, JSONPath assertions, response validation, and Maven/Gradle integration. Use when working with rest assured bdd, api or when the user mentions rest assured bdd, api."
---

Expert Java REST API testing reference with Given/When/Then flows, JSONPath assertions, response validation, and Maven/Gradle integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn dependency:get -Dartifact=io.rest-assured:rest-assured:5`
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

**Parameters:**
- `baseURI` (string): RestAssured.baseURI, e.g. http://localhost:8080
- `port` (integer): RestAssured.port when not 80/443
- `jsonPath` (string): GPath expression like data.items[0].id

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

## References
- [Rest Assured docs](https://github.com/rest-assured/rest-assured/wiki/Usage)
- [Rest Assured on Maven Central](https://central.sonatype.com/artifact/io.rest-assured/rest-assured)
