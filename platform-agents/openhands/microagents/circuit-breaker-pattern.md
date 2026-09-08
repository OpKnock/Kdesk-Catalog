---
name: "circuit-breaker-pattern"
description: "Implement the circuit breaker pattern in Java with Resilience4j and in Go with gobreaker, including thresholds and fallbacks. Use when working with resilience4j, gobreaker, api or when the user mentions resilience4j, gobreaker, api."
type: knowledge
triggers: ["circuit-breaker-pattern", "resilience4j", "gobreaker"]
---

Implement the circuit breaker pattern in Java with Resilience4j and in Go with gobreaker, including thresholds and fallbacks.

## Agentic Workflow: Read -> Reason -> Act (circuit-breaker-pattern)

You are **Circuit Breaker Pattern** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `circuit-breaker-pattern`
- Domain: Implement the circuit breaker pattern in Java with Resilience4j and in Go with gobreaker, including thresholds and fallbacks.
- **resilience4j**: Add circuit breakers to Java apps with Resilience4j and configure thresholds — `mvn dependency:get -Dartifact=io.github.resilience4j:resilience4j-circuitbreaker`
- **gobreaker**: Use sony/gobreaker circuit breaker in Go services with custom thresholds and fallbacks — `go get github.com/sony/gobreaker`
- Check `knowledge` and `prerequisites: mvn`

### 2. Reason — think for `circuit-breaker-pattern`
- For `resilience4j`: Add circuit breakers to Java apps with Resilience4j and configure thresholds — decide which checks to run
- For `gobreaker`: Use sony/gobreaker circuit breaker in Go services with custom thresholds and fallbacks — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `circuit-breaker-pattern` tools
- Tools: `Glob`, `Grep`, `Read`, `Mvn`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `circuit-breaker-pattern:8a0ae5db`

# Circuit Breaker Pattern

Protect APIs from cascading failures with circuit breakers.

## When to Use

- A downstream dependency is failing or slow
- Preventing timeouts from piling up on a flaky service
- Fast-failing with fallbacks instead of hanging

## States

Closed -> (failure ratio exceeded) -> Open -> (timeout) -> Half-open -> (success) -> Closed

## Java with Resilience4j

```xml
<dependency>
  <groupId>io.github.resilience4j</groupId>
  <artifactId>resilience4j-circuitbreaker</artifactId>
  <version>2.2.0</version>
</dependency>
```

```java
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(60)
    .waitDurationInOpenState(Duration.ofSeconds(10))
    .slidingWindowSize(20)
    .build();
CircuitBreaker cb = CircuitBreaker.of("payments", config);
String result = cb.executeSupplier(() -> paymentsClient.charge(order));
```

## Go with gobreaker

```go
st := gobreaker.Settings{
  Name: "payments",
  MaxRequests: 5,
  Interval: 60 * time.Second,
  Timeout: 10 * time.Second,
  ReadyToTrip: func(counts gobreaker.Counts) bool {
    return counts.ConsecutiveFailures > 5
  },
}
cb := gobreaker.NewCircuitBreaker(st)
resp, err := cb.Execute(func() (interface{}, error) {
  return charge(order)
})
```

## Testing

```bash
# Open the circuit by failing repeatedly, then confirm fast-fail
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/payments
# Load to trigger thresholds
hey -n 200 -c 20 http://localhost:8080/api/payments
```

## Best Practices

- Tune thresholds from observed p99 and error budgets
- Provide fallbacks for degraded mode
- Expose breaker state as metrics
- Set a probe timeout to recover automatically
- Do not place breakers between a client and its own gateway
- Test the open, half-open, and closed transitions explicitly

## Capabilities

### resilience4j
Add circuit breakers to Java apps with Resilience4j and configure thresholds

**Parameters:**
- `artifact` (string): Resilience4j artifact coordinate
- `version` (string): Resilience4j version such as 2.2.0

**Commands:**
- `mvn dependency:get -Dartifact=io.github.resilience4j:resilience4j-circuitbreaker:2.2.0`
- `mvn dependency:get -Dartifact=io.github.resilience4j:resilience4j-spring-boot3:2.2.0`
- `mvn test`
- `mvn spring-boot:run`

**Examples:**
- mvn dependency:get -Dartifact=io.github.resilience4j:resilience4j-circuitbreaker:2.2.0
- mvn test -Dtest=CircuitBreakerTest
- mvn spring-boot:run

### gobreaker
Use sony/gobreaker circuit breaker in Go services with custom thresholds and fallbacks

**Parameters:**
- `failure_ratio` (string): Failure ratio that opens the circuit, e.g. 0.6
- `timeout` (string): Timeout before probing closed again, e.g. 10s

**Commands:**
- `go get github.com/sony/gobreaker`
- `go run ./cmd/server`
- `go test ./...`
- `go vet ./...`

**Examples:**
- go get github.com/sony/gobreaker
- go test -run TestBreaker -v ./...
- go run ./cmd/server

## References
- [Resilience4j Docs](https://resilience4j.readme.io/)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
