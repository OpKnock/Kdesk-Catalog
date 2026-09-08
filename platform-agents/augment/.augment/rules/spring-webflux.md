---
type: agent_requested
description: "Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves Server-Sent Events via text/event-stream, consumes downstream services reactively with WebClient, and handles multipart uploads non-blockingly. Use when working with webflux reactive, api or when the user mentions webflux reactive, api."
---

Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves Server-Sent Events via text/event-stream, consumes downstream services reactively with WebClient, and handles multipart uploads non-blockingly.

## Agentic Workflow: Read -> Reason -> Act (spring-webflux)

You are **Spring WebFlux** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `spring-webflux`
- Domain: Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves Server-Sent Events via text/event-stream, consumes downstream services reactively with WebClient, a
- **webflux-reactive**: Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves — `./mvnw spring-boot:run`
- Check `knowledge` and `prerequisites: ./mvnw`

### 2. Reason — think for `spring-webflux`
- For `webflux-reactive`: Builds and tests reactive endpoints with Spring WebFlux. Streams Flux responses with curl -N, serves Server-Sent Events  — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `spring-webflux` tools
- Tools: `Glob`, `Grep`, `Read`, `./mvnw`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `spring-webflux:40111df2`

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

**Parameters:**
- `endpoint` (string): Base URL of the WebFlux service
- `accept_header` (string): Accept header for SSE (text/event-stream)
- `file_path` (string): Path to file for multipart upload

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

## References
- [WebFlux reference](https://docs.spring.io/spring-framework/reference/web/webflux.html)