---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Implement resilience patterns with Hystrix-style circuit breakers in Go (hystrix-go/gobreaker), with load-test verification.

## Agentic Workflow: Read -> Reason -> Act (circuit-breaker)

You are **Circuit Breaker** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `circuit-breaker`
- Domain: Implement resilience patterns with Hystrix-style circuit breakers in Go (hystrix-go/gobreaker), with load-test verification.
- **hystrix-go**: Add circuit breaking and fallbacks to Go APIs with hystrix-go — `go get github.com/afex/hystrix-go/hystrix`
- **load-verify**: Load-test the service to trigger and observe breaker transitions — `hey -n 500 -c 50 http://localhost:8080/api/payments`
- Check `knowledge` and `prerequisites: hey`

### 2. Reason — think for `circuit-breaker`
- For `hystrix-go`: Add circuit breaking and fallbacks to Go APIs with hystrix-go — decide which checks to run
- For `load-verify`: Load-test the service to trigger and observe breaker transitions — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `circuit-breaker` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Hey` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `circuit-breaker:06113d0e`

# Circuit Breaker

Protect API consumers from slow or failing dependencies.

## When to Use

- Downstream services are flaky or slow
- Preventing request pileups and cascading failures
- Graceful degradation with fallbacks

## hystrix-go

```go
package main

import (
  "github.com/afex/hystrix-go/hystrix"
)

func init() {
  hystrix.ConfigureCommand("payments-api", hystrix.CommandConfig{
    Timeout:                2000,
    MaxConcurrentRequests:  100,
    ErrorPercentThreshold:  50,
    RequestVolumeThreshold: 10,
    SleepWindow:            10000,
  })
}

func charge(orderID string) (string, error) {
  out, err := hystrix.Do("payments-api", func() (interface{}, error) {
    return paymentsClient.charge(orderID)
  }, func(err error) (interface{}, error) {
    return "fallback", nil
  })
  return out.(string), err
}
```

```bash
go get github.com/afex/hystrix-go/hystrix
go run ./cmd/server
```

## Trigger the Breaker

```bash
# Fail the downstream, then flood the endpoint
hey -n 500 -c 50 http://localhost:8080/api/payments
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/payments
```

## Metrics

Hystrix metrics stream on http://localhost:8070/hystrix.stream; run a dashboard or scrape it.

## Testing

```bash
go test -run TestCircuitBreaker -v ./...
go test -race ./...
```

## Best Practices

- Set ErrorPercentThreshold based on your error budget
- Tune RequestVolumeThreshold to avoid tripping on noise
- Always provide a fallback function
- Expose breaker state to monitoring
- SleepWindow should exceed downstream recovery time
- Test open, half-open, and closed transitions explicitly
- Combine with timeouts and retries, not instead of them

## Capabilities

### hystrix-go
Add circuit breaking and fallbacks to Go APIs with hystrix-go

**Parameters:**
- `command_name` (string): Hystrix command name, e.g. payments-api
- `timeout_ms` (string): Command timeout in milliseconds

**Commands:**
- `go get github.com/afex/hystrix-go/hystrix`
- `go run ./cmd/server`
- `go test ./...`
- `go vet ./...`

**Examples:**
- go get github.com/afex/hystrix-go/hystrix
- go test -v ./...
- go run ./cmd/server

### load-verify
Load-test the service to trigger and observe breaker transitions

**Parameters:**
- `requests` (string): Total requests for the load test
- `concurrency` (string): Concurrent workers

**Commands:**
- `hey -n 500 -c 50 http://localhost:8080/api/payments`
- `hey -n 500 -c 50 -m POST -H "Content-Type: application/json" -d '{}' http://localhost:8080/api/payments`
- `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/payments`
- `go test -run TestCircuitBreaker -v ./...`

**Examples:**
- hey -n 500 -c 50 http://localhost:8080/api/payments
- curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/payments
- go test -run TestCircuitBreaker -v ./...

## References
- [hystrix-go GitHub](https://github.com/afex/hystrix-go)
- [Resilience Patterns](https://github.com/Resilience4J/resilience4j)
