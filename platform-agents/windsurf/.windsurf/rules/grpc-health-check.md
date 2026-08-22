---
trigger: glob
description: "gRPC health checking protocol: probing services with grpc_health_probe and grpcurl against the grpc.health.v1.Health service, including per-service checks."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Grpc Health Check

gRPC health checking protocol: probing services with grpc_health_probe and grpcurl against the grpc.health.v1.Health service, including per-service checks.

## Instructions

# gRPC Health Check

Probe gRPC services with the standard health protocol.

## What this skill does

- Checks overall and per-service health of gRPC endpoints.
- Runs health probes as Kubernetes liveness/readiness probes.
- Interprets SERVING, NOT_SERVING, and UNKNOWN statuses.
- Wires the health service into Go servers via the grpc_health_probe package.

## When to use

- A Kubernetes deployment with a gRPC app needs liveness/readiness probes.
- A load balancer needs health signals that speak gRPC, not HTTP.
- Debugging why a service is not receiving traffic.

## Real commands

```bash
# Install the probe
go install github.com/grpc-ecosystem/grpc-health-probe/cmd/grpc_health_probe@latest

# Check overall health
grpc_health_probe -addr=localhost:50051

# Check a specific service
grpc_health_probe -addr=localhost:50051 -service helloworld.Greeter

# With gRPC reflection, query the health service directly
grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check
grpcurl -plaintext -d '{"service":"helloworld.Greeter"}' localhost:50051 grpc.health.v1.Health/Check
```

## Server wiring (Go)

```go
import "google.golang.org/grpc/health"
import healthpb "google.golang.org/grpc/health/grpc_health_v1"

hs := health.NewServer()
hs.SetServingStatus("helloworld.Greeter", healthpb.HealthCheckResponse_SERVING)
healthpb.RegisterHealthServer(s, hs)
```

## Kubernetes probe

```yaml
livenessProbe:
  exec:
    command: ["/bin/grpc_health_probe", "-addr=:50051"]
  initialDelaySeconds: 10
readinessProbe:
  exec:
    command: ["/bin/grpc_health_probe", "-addr=:50051", "-service", "helloworld.Greeter"]
```

## Testing

```bash
go run ./server &
grpc_health_probe -addr=localhost:50051 && echo HEALTHY
grpc_health_probe -addr=localhost:50051 -service does.not.Exist; echo "exit=$?"  # non-zero
```

## Best practices

- Register per-service status when your binary hosts multiple gRPC services.
- Report NOT_SERVING while the service is starting or shutting down.
- Use `-connect-timeout` to bound probe time in Kubernetes.
- The probe exits non-zero when unhealthy: perfect for `exec` probes.

## Example exchange

```
User: The pod is marked healthy but not ready.
Agent: Add a readiness probe for the specific service:
       grpc_health_probe -addr=:50051 -service helloworld.Greeter
```

## Capabilities

### health-probing
Probe gRPC endpoints for health status using the standard grpc.health.v1.Health protocol.

**Commands:**
- `grpc_health_probe -addr=localhost:50051`
- `grpc_health_probe -addr=localhost:50051 -service helloworld.Greeter`
- `grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check`
- `grpcurl -plaintext -d '{"service":"helloworld.Greeter"}' localhost:50051 grpc.health.v1.Health/Check`
- `go install github.com/grpc-ecosystem/grpc-health-probe/cmd/grpc_health_probe@latest`

**Examples:**
- grpc_health_probe -addr=localhost:50051 -connect-timeout 5s
- kubectl exec deployment/myapp -- grpc_health_probe -addr=:50051
- grpcurl -plaintext localhost:50051 list | grep health
