---
type: agent_requested
description: "Test Ktor applications: testApplication-based integration tests, client requests against routes, and assertions on status/JSON responses. Use when working with integration tests, route assertions, api or when the user mentions integration tests, route assertions, api."
---

Test Ktor applications: testApplication-based integration tests, client requests against routes, and assertions on status/JSON responses.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `./gradlew test`, `curl -s http://localhost:8080/hello`
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

# Ktor Testing

Integration-test Ktor applications with testApplication.

## What this skill does

- Boots the app in-process with testApplication.
- Sends real requests through the routing via the test client.
- Asserts status codes, headers, and JSON bodies.

## When to use

- Verifying routes and plugins before release.
- Testing auth, content negotiation, and error pages.
- Keeping test feedback loops fast (no external server).

## Real commands

```bash
# Run all tests
./gradlew test

# Single class
./gradlew test --tests 'com.example.ApplicationTest'

# Pattern with stacktrace
./gradlew test --tests '*Auth*' --stacktrace

# Manual smoke against a running app
./gradlew run &
curl -s http://localhost:8080/hello
```

## Test example

```kotlin
class ApplicationTest {
    @Test
    fun `GET hello returns 200`() = testApplication {
        application { module() }
        client.get("/hello").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertEquals("Hello, world!", bodyAsText())
        }
    }

    @Test
    fun `unknown route returns 404`() = testApplication {
        application { module() }
        assertEquals(HttpStatusCode.NotFound, client.get("/nope").status)
    }
}
```

## Testing

```bash
./gradlew test --tests 'com.example.ApplicationTest'
```

## Best practices

- Use testApplication per suite; share setup in @BeforeTest.
- Assert status AND body; status alone hides content regressions.
- Test auth routes with both valid and invalid credentials.

## Capabilities

### integration-tests
Write and run testApplication integration tests for routes.

**Parameters:**
- `test_class` (string): Test class filter pattern.
- `stacktrace` (boolean): Print full stack traces on failure.

**Commands:**
- `./gradlew test`
- `./gradlew test --tests 'com.example.ApplicationTest'`
- `./gradlew test --info`
- `./gradlew test --tests '*Auth*' --stacktrace`

**Examples:**
- ./gradlew test
- ./gradlew test --tests 'com.example.ApplicationTest'
- ./gradlew test --tests '*Auth*' --stacktrace

### route-assertions
Drive routes with test client and assert status and bodies.

**Parameters:**
- `path` (string): Route under test.

**Commands:**
- `curl -s http://localhost:8080/hello`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/hello`
- `./gradlew test --tests 'com.example.RoutesTest'`

**Examples:**
- curl -s http://localhost:8080/hello
- ./gradlew test --tests 'com.example.RoutesTest'

## References
- [Ktor Testing](https://ktor.io/docs/server-testing.html)
- [Ktor TestClient](https://ktor.io/docs/server-testing-kotest.html)