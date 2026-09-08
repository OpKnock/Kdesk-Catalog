---
trigger: glob
description: "Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence, reads sidecar logs and local stats endpoints, and runs standalone Envoy for local proxy configuration iteration. Use when working with sidecar ops, api or when the user mentions sidecar ops, api."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence, reads sidecar logs and local stats endpoints, and runs standalone Envoy for local proxy configuration iteration.

## Agentic Workflow: Read -> Reason -> Act (sidecar-pattern)

You are **Sidecar Pattern** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `sidecar-pattern`
- Domain: Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence, reads sidecar logs and local stats endpoints, and runs standalone Envoy for local proxy configurat
- **sidecar-ops**: Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence — `kubectl get pods -l app=api -o jsonpath='{.items[0].spec.containers[*].name}'`
- Check `knowledge` and `prerequisites: envoy, kubectl`

### 2. Reason — think for `sidecar-pattern`
- For `sidecar-ops`: Operates sidecar containers in Kubernetes pods. Inspects container lists to confirm sidecar presence, reads sidecar logs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sidecar-pattern` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Envoy` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sidecar-pattern:83e9db99`

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

**Parameters:**
- `pod_name` (string): Kubernetes pod name containing the sidecar
- `sidecar_name` (string): Sidecar container name (e.g., istio-proxy)
- `config_path` (string): Path to Envoy config file for local testing

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

## References
- [Azure sidecar pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar)
