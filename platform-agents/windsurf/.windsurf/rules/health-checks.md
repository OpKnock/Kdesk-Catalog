---
trigger: glob
description: "Implements liveness, readiness, and startup probes across Kubernetes, Docker, and HTTP endpoints with proper semantics."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Health Checks

Implements liveness, readiness, and startup probes across Kubernetes, Docker, and HTTP endpoints with proper semantics.

## Instructions

# Health Checks

Implement liveness, readiness, and startup probes correctly.

## When to Use

- Every deployed service should expose health endpoints
- Kubernetes orchestration for restart and traffic decisions
- Load balancers deciding when to take instances out of rotation
- Distributed systems that need dependency status visibility

## Endpoint Semantics

- /health/live (liveness): process is alive; restart if failing
- /health/ready (readiness): can serve traffic; drop from LB if failing
- /health/startup: slow-starting apps; gates the other probes

## Commands

```bash
# Test endpoints
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health
curl -sf http://localhost:8000/ready && echo OK

# Kubernetes
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl describe pod -l app=myapp
kubectl get pods -w
```

## Probe Example

```yaml
# deployment.yaml (excerpt)
containers:
  - name: myapp
    image: myapp:1.2.3
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8080
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8080
      initialDelaySeconds: 5
    startupProbe:
      httpGet:
        path: /health/startup
        port: 8080
      failureThreshold: 30
```

## Best Practices

- Readiness should check real dependencies with timeouts and caching
- Never let a health check take longer than the probe timeout
- Return 503 with a body describing which dependency is down
- Keep health endpoints cheap; do not run full DB queries every probe
- Use startup probes for apps that need >10s to boot
- Alert on readiness failures separately from liveness restarts

## Capabilities

### http-health
Create and test HTTP health endpoints.

**Commands:**
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health`
- `curl -s http://localhost:8000/ready`
- `curl -s http://localhost:8000/live`
- `python -m http.server 8080`

**Examples:**
- curl -s -o /dev/null -w "%{http_code} %{time_total}" http://localhost:8000/health
- curl -sf http://localhost:8000/ready && echo OK

### k8s-probes
Define liveness, readiness, and startup probes in Kubernetes manifests.

**Commands:**
- `kubectl apply -f deployment.yaml`
- `kubectl get pods -w`
- `kubectl describe pod myapp-abc123`
- `kubectl rollout status deployment/myapp`

**Examples:**
- kubectl get deploy myapp -o jsonpath="{.spec.template.spec.containers[0].readinessProbe}"
- kubectl describe pod -l app=myapp | grep -A5 Probes
