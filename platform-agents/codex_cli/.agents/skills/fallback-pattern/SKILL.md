---
name: "fallback-pattern"
description: "Resilience patterns for API durability: circuit breakers that halt calls to failing dependencies, retries with exponential backoff and jitter for transient errors, timeout bounds on outbound requests, and cached fallback responses so degraded answers still succeed."
---

# Fallback Pattern

Resilience patterns for API durability: circuit breakers that halt calls to failing dependencies, retries with exponential backoff and jitter for transient errors, timeout bounds on outbound requests, and cached fallback responses so degraded answers still succeed.

## Instructions

# Fallback Pattern

## What this skill does

Fallback patterns keep the API alive when dependencies fail: circuit breakers stop calls to a dead service, retries with backoff absorb transient errors, timeouts bound slow calls, and fallback values serve degraded responses.

## When to use

- A downstream service is down and requests pile up
- Designing for partial outages instead of total failure
- Adding resilience to third-party API calls

## Real commands

```bash
# Observe current behavior
curl -s http://localhost:8080/api/orders | jq '.source'

# Health shows the circuit state
curl -s http://localhost:8080/actuator/health | jq '.components.ordersCircuit'

# Node fallback demo
node -e "const f=require('p-retry');f(async()=>{const r=await fetch('http://db:5432');if(!r.ok)throw new Error('down')},{retries:3,minTimeout:500}).catch(e=>console.log('fallback: cached data'))"
```

## Circuit breaker config (Resilience4j)

```yaml
resilience4j.circuitbreaker:
  instances:
    orders:
      failureRateThreshold: 50
      waitDurationInOpenState: 10s
      slidingWindowSize: 20
      recordExceptions:
        - java.io.IOException
```

## Fallback handler example (Java)

```java
@CircuitBreaker(name = "orders", fallbackMethod = "ordersFallback")
public List<Order> getOrders() {
    return ordersClient.fetch();
}

public List<Order> ordersFallback(Throwable t) {
    return cache.read("orders"); // degraded response
}
```

## Testing

```bash
# Kill the dependency, then verify the circuit opens
systemctl stop orders-db
sleep 5
curl -s http://localhost:8080/actuator/health | jq '.components.ordersCircuit'
```

## Best practices

- Always provide a fallback; never let a dependency failure bubble to 5xx when a degraded answer exists.
- Retry only on transient errors, with jittered exponential backoff.
- Timeouts must be shorter than the circuit breaker's wait window.
- Cache last-known-good data for fallback reads.
- Monitor open/closed state and fallback invocation rate.

## Capabilities

### resilience-patterns
Configure and test circuit breakers and fallbacks in Java (Resilience4j) and verify behavior.

**Commands:**
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/orders`
- `curl -s http://localhost:8080/api/orders | jq '.source'`
- `node -e "const f=require('p-retry');f(async()=>{const r=await fetch('http://db:5432');if(!r.ok)throw new Error('down')},{retries:3,minTimeout:500}).catch(e=>console.log('fallback: cached data'))"`
- `grep -rn 'CircuitBreaker' src/ | head -10`
- `curl -s http://localhost:8080/actuator/health | jq '.components.ordersCircuit'`

**Examples:**
- curl -s http://localhost:8080/api/orders | jq '.source'
- curl -s http://localhost:8080/actuator/health | jq '.components.ordersCircuit'
- grep -rn 'CircuitBreaker' src/ | head -10
