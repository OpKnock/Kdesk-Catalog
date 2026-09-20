---
type: agent_requested
description: "Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves Server-Sent Events via text/event-stream, consumes downstream services reactively with WebClient, and handles multipart uploads non-blockingly."
---

# Spring WebFlux

Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves Server-Sent Events via text/event-stream, consumes downstream services reactively with WebClient, and handles multipart uploads non-blockingly.

## Instructions

# Spring WebFlux

Hand-crafted skill for reactive Spring WebFlux APIs.

## What this skill does

- Builds non-blocking endpoints returning Flux and Mono
- Streams data with curl -N and SSE via text/event-stream
- Consumes services reactively with WebClient

## When to use

- High-concurrency APIs that outgrow thread-per-request
- Streaming responses to clients as data arrives
- Chaining async calls without blocking threads

## Real commands

```bash
# Run the app
./mvnw spring-boot:run

# Stream a Flux response as it is emitted
curl -N localhost:8080/flux

# SSE events
curl -H 'Accept: text/event-stream' -N localhost:8080/events

# JSON list
curl -s localhost:8080/api/prices | jq 'length'

# Multipart upload via WebFlux
curl -s -X POST localhost:8080/upload -F 'file=@data.csv'
```

## Controller example

```java
@RestController
public class ReactiveController {

    @GetMapping(value = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> events() {
        return Flux.interval(Duration.ofSeconds(1)).map(i -> "tick " + i);
    }

    @GetMapping("/api/prices")
    public Mono<List<BigDecimal>> prices() {
        return webClient.get().uri("/prices").retrieve().bodyToFlux(BigDecimal.class).collectList();
    }
}
```

## Testing

```bash
curl -N localhost:8080/flux | head -5
curl -H 'Accept: text/event-stream' -N localhost:8080/events | head -3
```

## Best practices

- Never block inside reactive chains: no Thread.sleep or blocking JDBC
- Add backpressure-aware limits on unbounded streams
- Use WebClient with timeouts for every downstream call

## Capabilities

### webflux-reactive
Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves Server-Sent Events via text/event-stream, consumes downstream services reactively with WebClient, and handles multipart uploads non-blockingly.

**Commands:**
- `./mvnw spring-boot:run`
- `curl -N localhost:8080/flux`
- `curl -H "Accept: text/event-stream" -N localhost:8080/events`
- `curl -s localhost:8080/api/prices | jq 'length'`
- `curl -s -X POST localhost:8080/upload -F "file=@data.csv"`

**Examples:**
- curl -N localhost:8080/flux
- curl -H "Accept: text/event-stream" -N localhost:8080/events
- curl -s localhost:8080/api/prices | jq 'length'
- curl -s -X POST localhost:8080/upload -F "file=@data.csv"