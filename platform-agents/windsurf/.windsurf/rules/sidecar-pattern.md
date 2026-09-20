---
trigger: glob
description: "Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence, reads sidecar logs and local stats endpoints, and runs standalone Envoy for local proxy configuration iteration."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Sidecar Pattern

Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence, reads sidecar logs and local stats endpoints, and runs standalone Envoy for local proxy configuration iteration.

## Instructions

# Sidecar Pattern

Hand-crafted skill for operating sidecar containers in Kubernetes.

## What this skill does

- Lists containers inside a pod to confirm the sidecar
- Reads sidecar logs and hits its local stats endpoints
- Runs standalone envoy with a custom config for local testing

## When to use

- Verifying istio-proxy or log-shipper sidecars are healthy
- Debugging a sidecar that restarts in a crash loop
- Prototyping a proxy sidecar locally before deploying

## Real commands

```bash
# What containers run in the pod?
kubectl get pods -l app=api -o jsonpath='{.items[0].spec.containers[*].name}'

# Sidecar logs
kubectl logs pod/api-7d9f -c istio-proxy --tail=50

# Stats from inside the sidecar
kubectl exec -it pod/api-7d9f -c istio-proxy -- curl -s localhost:15090/stats/prometheus | head -5

# Health check endpoint of the sidecar
kubectl exec -it pod/api-7d9f -c istio-proxy -- curl -s localhost:15020/healthz

# Standalone envoy for local config iteration
envoy --config-path envoy.yaml
```

## Pod spec

```yaml
spec:
  containers:
    - name: api
      image: ghcr.io/example/api:v2.1
    - name: istio-proxy
      image: proxyv2
```

## Testing

```bash
kubectl logs pod/api-7d9f -c istio-proxy --tail=20
kubectl exec -it pod/api-7d9f -c istio-proxy -- curl -s localhost:15090/stats/prometheus | grep istio_requests_total | head
```

## Best practices

- Give every sidecar a name and liveness probe in the pod spec
- Share volumes and localhost networking between app and sidecar
- Never let the app depend on the sidecar being the source of truth

## Capabilities

### sidecar-ops
Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence, reads sidecar logs and local stats endpoints, and runs standalone Envoy for local proxy configuration iteration.

**Commands:**
- `kubectl get pods -l app=api -o jsonpath='{.items[0].spec.containers[*].name}'`
- `kubectl logs pod/api-7d9f -c istio-proxy --tail=50`
- `kubectl exec -it pod/api-7d9f -c istio-proxy -- curl -s localhost:15090/stats/prometheus`
- `kubectl exec -it pod/api-7d9f -c istio-proxy -- curl -s localhost:15020/healthz`
- `envoy --config-path envoy.yaml`

**Examples:**
- kubectl get pods -l app=api -o jsonpath='{.items[0].spec.containers[*].name}'
- kubectl logs pod/api-7d9f -c istio-proxy --tail=50
- kubectl exec -it pod/api-7d9f -c istio-proxy -- curl -s localhost:15020/healthz
- envoy --config-path envoy.yaml
