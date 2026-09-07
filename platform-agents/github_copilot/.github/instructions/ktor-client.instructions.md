---
applyTo: "**/*.go **/*.json **/*.kt **/*.r **/*.sh"
---

Make HTTP calls from Ktor applications with ktor-client: engine selection, serialization plugins, and timeouts for API integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gradle dependencies --configuration runtimeClasspath | grep `, `curl -s http://localhost:8080/proxy | jq .`
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

# Ktor Client

Make typed HTTP calls from Ktor applications.

## What this skill does

- Configures HttpClient with an engine and content negotiation.
- Uses Json plugin for typed request/response bodies.
- Handles timeouts and non-2xx responses.

## When to use

- Kotlin services calling other APIs (REST or gRPC-json).
- Building BFF routes that proxy upstream services.
- Testing API clients with Ktor test infrastructure.

## Real commands

```bash
# Verify dependencies resolved
gradle dependencies --configuration runtimeClasspath | grep ktor-client

# Run the app that makes outbound calls
./gradlew run

# Exercise the proxy route
curl -s http://localhost:8080/proxy | jq .

# Error mapping: upstream 404 -> 502
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/proxy-404

# Timeout behavior
curl -s http://localhost:8080/proxy-timeout
```

## Client example

```kotlin
val client = HttpClient(CIO) {
    install(ContentNegotiation) {
        json(Json { ignoreUnknownKeys = true })
    }
    install(HttpTimeout) {
        requestTimeoutMillis = 5_000
        connectTimeoutMillis = 2_000
    }
    defaultRequest {
        contentType(ContentType.Application.Json)
    }
}

suspend fun fetchOrder(id: String): Order =
    client.get("https://api.example.com/orders/$id").body()
```

## Testing

```bash
./gradlew test
```

## Best practices

- Install HttpTimeout; clients without timeouts hang requests.
- Use expectSuccess = true and catch ClientRequestException/ServerResponseException.
- Reuse one HttpClient per application; don't create per request.

## Capabilities

### client-setup
Add ktor-client dependencies and configure an engine with plugins.

**Parameters:**
- `engine` (string): Client engine: CIO, OkHttp, Apache, Java.
- `endpoint` (string): Proxy endpoint that exercises the client.

**Commands:**
- `gradle dependencies --configuration runtimeClasspath | grep ktor-client`
- `./gradlew run`
- `curl -s http://localhost:8080/proxy`
- `./gradlew build`

**Examples:**
- gradle dependencies --configuration runtimeClasspath | grep ktor-client
- ./gradlew run
- curl -s http://localhost:8080/proxy

### call-verify
Verify outbound calls: status, JSON body, and error mapping.

**Parameters:**
- `path` (string): App route that triggers an outbound client call.

**Commands:**
- `curl -s http://localhost:8080/proxy | jq .`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/proxy-404`
- `curl -s http://localhost:8080/proxy-timeout`
- `./gradlew test`

**Examples:**
- curl -s http://localhost:8080/proxy | jq .
- curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/proxy-404
- ./gradlew test

## References
- [Ktor Client](https://ktor.io/docs/client-create-new-application.html)
- [Ktor Client Serialization](https://ktor.io/docs/client-serialization.html)
