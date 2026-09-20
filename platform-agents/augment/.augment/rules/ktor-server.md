---
type: agent_requested
description: "Build Ktor server applications: routing, content negotiation, static files, and deployment as a standalone JVM app. Use when working with server routes, json api or when the user mentions server routes, json api."
---

Build Ktor server applications: routing, content negotiation, static files, and deployment as a standalone JVM app.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `./gradlew run`, `curl -s http://localhost:8080/api/orders/42 | jq .`
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

# Ktor Server

Build production Ktor server applications.

## What this skill does

- Sets up routing with typed handlers.
- Serves JSON via ContentNegotiation.
- Packages and runs the standalone JAR.

## When to use

- New Kotlin backend services.
- Lightweight REST APIs with coroutine support.
- Services needing static files + JSON APIs.

## Real commands

```bash
# Run in dev
./gradlew run

# Build a runnable fat jar (shadow plugin)
./gradlew build
java -jar build/libs/ktor-server-all.jar

# Test routes
curl -s http://localhost:8080/hello
curl -s http://localhost:8080/api/orders/42 | jq .
curl -s -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"id":43,"amount":99.5}'
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/orders/notfound
```

## Routing example

```kotlin
fun Application.module() {
    install(ContentNegotiation) { json() }
    routing {
        get("/hello") { call.respondText("Hello, world!") }
        get("/api/orders/{id}") {
            val id = call.parameters["id"]
            val order = ordersRepo.findById(id)
            if (order == null) call.respond(HttpStatusCode.NotFound)
            else call.respond(order)
        }
        post("/api/orders") {
            val order = call.receive<Order>()
            ordersRepo.save(order)
            call.respond(HttpStatusCode.Created, order)
        }
    }
}
```

## Testing

```bash
./gradlew test
```

## Best practices

- Use Ktor's status pages plugin to centralize error responses.
- Serve behind a proxy (nginx/haproxy) for TLS termination.
- Set engine config (threads, queue size) for production throughput.

## Capabilities

### server-routes
Define Ktor routes and run the server.

**Parameters:**
- `port` (integer): Listen port, default 8080.
- `route` (string): Route path to test.

**Commands:**
- `./gradlew run`
- `./gradlew build`
- `java -jar build/libs/ktor-server-all.jar`
- `curl -s http://localhost:8080/hello`

**Examples:**
- ./gradlew run
- java -jar build/libs/ktor-server-all.jar
- curl -s http://localhost:8080/hello

### json-api
Serve JSON APIs with content negotiation and test them.

**Parameters:**
- `method` (string): HTTP method.
- `body` (string): JSON body for POST/PUT.

**Commands:**
- `curl -s http://localhost:8080/api/orders/42 | jq .`
- `curl -s -X POST http://localhost:8080/api/orders -H 'Content-Type: application/json' -d '{"id":43,"amount":99.5}'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/orders/notfound`
- `./gradlew test`

**Examples:**
- curl -s http://localhost:8080/api/orders/42 | jq .
- curl -s -X POST http://localhost:8080/api/orders -H 'Content-Type: application/json' -d '{"id":43,"amount":99.5}'
- ./gradlew test

## References
- [Ktor Server](https://ktor.io/docs/server-create-a-new-project.html)
- [Ktor ContentNegotiation](https://ktor.io/docs/server-serialization.html)