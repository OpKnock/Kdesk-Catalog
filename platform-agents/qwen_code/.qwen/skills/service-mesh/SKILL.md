---
name: "service-mesh"
description: "Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, analyzes configuration, routes traffic with VirtualServices, and enables mTLS between services without application changes. Use when working with istio linkerd mesh, api or when the user mentions istio linkerd mesh, api."
license: "MIT"
compatibility: "Requires istioctl, kubectl, linkerd. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(istioctl:*) Bash(kubectl:*) Bash(linkerd:*)"
---

Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, analyzes configuration, routes traffic with VirtualServices, and enables mTLS between services without application changes.

## Agentic Workflow: Read -> Reason -> Act (service-mesh)

You are **Service Mesh** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `service-mesh`
- Domain: Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, analyzes configuration, routes traffic with VirtualServices, and enables mTLS between services without 
- **istio-linkerd-mesh**: Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, ana — `istioctl install --set profile=demo -y`
- Check `knowledge` and `prerequisites: istioctl, kubectl, linkerd`

### 2. Reason — think for `service-mesh`
- For `istio-linkerd-mesh`: Installs and operates Istio or Linkerd service meshes in Kubernetes. Verifies sidecar injection, analyzes configuration, — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `service-mesh` tools
- Tools: `Glob`, `Grep`, `Read`, `Istioctl`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `service-mesh:8169e2bf`

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

**Parameters:**
- `profile` (string): Istio installation profile (demo, default, minimal)
- `namespace` (string): Kubernetes namespace for mesh operations

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

## References
- [Istio docs](https://istio.io/latest/docs/)
