---
trigger: glob
description: "Build Ktor server applications: routing, content negotiation, static files, and deployment as a standalone JVM app."
globs: ["**/*.go", "**/*.java", "**/*.json", "**/*.kt", "**/*.r", "**/*.sh"]
---

# Ktor Server

Build Ktor server applications: routing, content negotiation, static files, and deployment as a standalone JVM app.

## Instructions

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

**Commands:**
- `curl -s http://localhost:8080/api/orders/42 | jq .`
- `curl -s -X POST http://localhost:8080/api/orders -H 'Content-Type: application/json' -d '{"id":43,"amount":99.5}'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/orders/notfound`
- `./gradlew test`

**Examples:**
- curl -s http://localhost:8080/api/orders/42 | jq .
- curl -s -X POST http://localhost:8080/api/orders -H 'Content-Type: application/json' -d '{"id":43,"amount":99.5}'
- ./gradlew test
