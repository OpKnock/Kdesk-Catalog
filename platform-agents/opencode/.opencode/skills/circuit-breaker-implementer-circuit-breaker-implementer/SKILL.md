---
name: "circuit-breaker-implementer-circuit-breaker-implementer"
description: "Implements circuit breakers and bulkheads in services with resilience4j, Hystrix-style patterns, and fallback strategies. Use when working with resilience4j, failure probing or when the user mentions resilience4j, failure probing."
---

Implements circuit breakers and bulkheads in services with resilience4j, Hystrix-style patterns, and fallback strategies.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn dependency:tree | grep resilience4j`, `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080`
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

# Circuit Breaker Implementer

Protect services from cascading failures.

## When to Use

- Calls to flaky or slow downstream services
- Preventing timeout pileups during outages
- Providing fast fallbacks when a dependency is down
- Isolating failure domains (bulkheads)

## States

- Closed: requests pass; failure rate tracked
- Open: fail fast; no calls to the dependency
- Half-open: limited trial calls to test recovery

## Config Example (resilience4j)

```yaml
resilience4j.circuitbreaker:
  instances:
    ordersApi:
      slidingWindowSize: 10
      failureRateThreshold: 50
      waitDurationInOpenState: 30s
      permittedNumberOfCallsInHalfOpenState: 3
      recordExceptions:
        - java.io.IOException
```

## Commands

```bash
# Check breaker state via actuator
curl -s http://localhost:8080/actuator/circuitbreakers
curl -s http://localhost:8080/actuator/health
curl -s http://localhost:8080/actuator/circuitbreakerevents

# Load test to observe transitions
ab -n 500 -c 20 http://localhost:8080/api/orders
```

## Java Example

```java
@CircuitBreaker(name = "ordersApi", fallbackMethod = "ordersFallback")
public List<Order> fetchOrders() {
    return ordersClient.getOrders();
}

public List<Order> ordersFallback(Exception ex) {
    return List.of(); // degraded response
}
```

## Best Practices

- Set failure thresholds from observed baseline error rates
- Keep waitDurationInOpenState long enough to let deps recover
- Always provide a fallback; never fail without one
- Record exceptions narrowly (timeouts, 5xx) not domain errors
- Combine with retry that has its own limits (retry then break)
- Expose breaker state in metrics and alert on transitions

## Capabilities

### resilience4j
Configure circuit breaker, retry, and bulkhead policies.

**Parameters:**
- `service` (string): Downstream service name
- `threshold` (number): Failure rate threshold

**Commands:**
- `mvn dependency:tree | grep resilience4j`
- `gradle dependencies | grep resilience4j`
- `curl -s http://localhost:8080/actuator/health`
- `curl -s http://localhost:8080/actuator/circuitbreakers`
- `curl -s http://localhost:8080/actuator/metrics/resilience4j.circuitbreaker.state`

**Examples:**
- curl -s http://localhost:8080/actuator/circuitbreakers | python -m json.tool
- curl -s http://localhost:8080/actuator/health | python -m json.tool

### failure-probing
Verify breaker behavior under failure.

**Parameters:**
- `endpoint` (string): Protected endpoint
- `concurrency` (integer): Concurrent requests for load probing

**Commands:**
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/orders`
- `ab -n 500 -c 20 http://localhost:8080/api/orders`
- `curl -s http://localhost:8080/actuator/circuitbreakerevents`
- `curl -s -H "Accept: application/json" http://localhost:8080/api/orders -w "\n%{http_code}"`

**Examples:**
- ab -n 500 -c 20 -H "Accept: application/json" http://localhost:8080/api/orders
- curl -s http://localhost:8080/actuator/circuitbreakerevents | python -m json.tool

## References
- [Resilience4j Docs](https://resilience4j.readme.io)
- [Circuit Breaker Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
