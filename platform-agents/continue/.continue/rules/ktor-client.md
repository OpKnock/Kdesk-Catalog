---
name: "Ktor Client"
description: "Make HTTP calls from Ktor applications with ktor-client: engine selection, serialization plugins, and timeouts for API integration. Use when working with client setup, call verify, api or when the user mentions client setup, call verify, api."
globs: ["**/*.go", "**/*.json", "**/*.kt", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Make HTTP calls from Ktor applications with ktor-client: engine selection, serialization plugins, and timeouts for API integration.

## Agentic Workflow: Read -> Reason -> Act (ktor-client)

You are **Ktor Client** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `ktor-client`
- Domain: Make HTTP calls from Ktor applications with ktor-client: engine selection, serialization plugins, and timeouts for API integration.
- **client-setup**: Add ktor-client dependencies and configure an engine with plugins. — `gradle dependencies --configuration runtimeClasspath | grep ktor-client`
- **call-verify**: Verify outbound calls: status, JSON body, and error mapping. — `curl -s http://localhost:8080/proxy | jq .`
- Check `knowledge` and `prerequisites: ./gradlew, gradle`

### 2. Reason — think for `ktor-client`
- For `client-setup`: Add ktor-client dependencies and configure an engine with plugins. — decide which checks to run
- For `call-verify`: Verify outbound calls: status, JSON body, and error mapping. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ktor-client` tools
- Tools: `Glob`, `Grep`, `Read`, `Gradle`, `./gradlew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ktor-client:b1f97148`

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