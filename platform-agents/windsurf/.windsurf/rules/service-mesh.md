---
trigger: glob
description: "Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, analyzes configuration, routes traffic with VirtualServices, and enables mTLS between services without application changes."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Service Mesh

Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, analyzes configuration, routes traffic with VirtualServices, and enables mTLS between services without application changes.

## Instructions

# Service Mesh

Hand-crafted skill for installing and operating a service mesh.

## What this skill does

- Installs Istio or Linkerd into a cluster
- Verifies proxies are connected and sidecars injected
- Routes traffic with VirtualService rules

## When to use

- Enabling mTLS between services without app changes
- Adding fine-grained traffic routing or canaries
- Rolling out mesh observability (metrics, tracing)

## Real commands

```bash
# Istio install (demo profile for evaluation)
istioctl install --set profile=demo -y

# Static analysis of your config
istioctl analyze

# Are proxies synced?
istioctl proxy-status

# Traffic rules
kubectl get virtualservices -A
kubectl get virtualservices -A -o yaml

# Linkerd bootstrap
linkerd check --pre && linkerd install | kubectl apply -f -
linkerd check
kubectl get deploy -n <ns> -o yaml | linkerd inject - | kubectl apply -f -
```

## VirtualService example

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routes
spec:
  hosts: [api]
  http:
    - match: [{ headers: { version: { exact: canary } } }]
      route: [{ destination: { host: api, subset: v2 } }]
    - route: [{ destination: { host: api, subset: v1 } }]
```

## Testing

```bash
istioctl proxy-status
kubectl exec deploy/api -c istio-proxy -- curl -s localhost:15090/stats/prometheus | grep istio_requests_total | head
```

## Best practices

- Run istioctl analyze before and after config changes
- Inject sidecars namespace-wide with labels, not pod by pod
- Validate mesh health with linkerd check or istioctl proxy-status

## Capabilities

### istio-linkerd-mesh
Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, analyzes configuration, routes traffic with VirtualServices, and enables mTLS between services without application changes.

**Commands:**
- `istioctl install --set profile=demo -y`
- `istioctl analyze`
- `istioctl proxy-status`
- `kubectl get virtualservices -A`
- `linkerd check --pre`
- `linkerd install`
- `linkerd check`

**Examples:**
- istioctl install --set profile=demo -y
- istioctl analyze
- istioctl proxy-status
- kubectl get virtualservices -A
- linkerd check --pre && linkerd install | kubectl apply -f -
