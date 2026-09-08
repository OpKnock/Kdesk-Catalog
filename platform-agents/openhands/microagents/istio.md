---
name: "istio"
description: "Installs and operates Istio service mesh: sidecar injection, VirtualService/DestinationRule traffic routing, mTLS, and traffic observation. Use when working with install and verify, traffic management, devops or when the user mentions install and verify, traffic management, devops."
type: knowledge
triggers: ["istio", "install-and-verify", "traffic-management"]
---

Installs and operates Istio service mesh: sidecar injection, VirtualService/DestinationRule traffic routing, mTLS, and traffic observation.

## Agentic Workflow: Read -> Reason -> Act (istio)

You are **istio** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `istio`
- Domain: Installs and operates Istio service mesh: sidecar injection, VirtualService/DestinationRule traffic routing, mTLS, and traffic observation.
- **install-and-verify**: Install the mesh, verify control plane health, and configure sidecar injection. — `istioctl install --set profile=demo`
- **traffic-management**: Configure VirtualService, DestinationRule, and Gateway resources for canary and weighted routing. — `kubectl apply -f virtualservice.yaml`
- Check `knowledge` and `prerequisites: istioctl, kubectl`

### 2. Reason — think for `istio`
- For `install-and-verify`: Install the mesh, verify control plane health, and configure sidecar injection. — decide which checks to run
- For `traffic-management`: Configure VirtualService, DestinationRule, and Gateway resources for canary and weighted routing. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `istio` tools
- Tools: `Glob`, `Grep`, `Read`, `Istioctl`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `istio:f39fc388`

# Istio Service Mesh

Deploy and manage Istio: sidecars, smart routing, mTLS, and mesh observability.

## What This Skill Does

- Installs Istio with profile-based operator manifests
- Enables namespace-wide or pod-level sidecar injection
- Routes traffic with VirtualService and DestinationRule (canary, weighted)
- Enforces mTLS with PeerAuthentication and AuthorizationPolicy
- Inspects Envoy proxy config via istioctl

## When to Use

- Rolling out a service mesh for mTLS and advanced routing
- Implementing canary releases with percentage splits
- Debugging routing mismatches (why traffic hits the wrong pod)

## Real Commands

```bash
# Install
istioctl install --set profile=demo -y
istioctl verify-install
istioctl analyze

# Injection
kubectl label namespace default istio-injection=enabled
kubectl rollout restart deployment/web

# Status
istioctl proxy-status
istioctl dashboard kiali
istioctl proxy-config route reviews-v1-abc | jq .name

# Traffic rules
kubectl apply -f virtualservice.yaml
kubectl apply -f destinationrule.yaml
kubectl apply -f gateway.yaml
```

## Canary VirtualService

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts: [reviews]
  http:
    - route:
        - destination: { host: reviews, subset: v1, weight: 90 }
        - destination: { host: reviews, subset: v2, weight: 10 }
```

## Best Practices

- Run `istioctl analyze` before and after every mesh change
- Prefer PeerAuthentication STRICT in production after rollout
- Use `istioctl experimental describe pod` as first debug step
- Verify injection: two containers per pod (istio-proxy sidecar)
- Keep Istio operator and CRD versions in sync with the CLI

## Capabilities

### install-and-verify
Install the mesh, verify control plane health, and configure sidecar injection.

**Parameters:**
- `profile` (string): Install profile: default, demo, minimal, external
- `namespace` (string): Namespace to enable injection on

**Commands:**
- `istioctl install --set profile=demo`
- `istioctl verify-install`
- `istioctl analyze`
- `kubectl label namespace default istio-injection=enabled`
- `istioctl proxy-status`
- `istioctl dashboard kiali`

**Examples:**
- istioctl install --set profile=demo -y
- istioctl analyze
- istioctl proxy-status

### traffic-management
Configure VirtualService, DestinationRule, and Gateway resources for canary and weighted routing.

**Parameters:**
- `pod` (string): Pod name for proxy-config inspection
- `manifest` (string): CR manifest file

**Commands:**
- `kubectl apply -f virtualservice.yaml`
- `kubectl apply -f destinationrule.yaml`
- `istioctl proxy-config route demo-pod`
- `istioctl proxy-config cluster demo-pod`
- `istioctl experimental describe pod demo-pod`
- `kubectl get virtualservices,destinationrules`

**Examples:**
- kubectl apply -f virtualservice.yaml
- istioctl proxy-config route reviews-v1-abc
- istioctl experimental describe pod reviews-v1-abc

## References
- [Istio Documentation](https://istio.io/latest/docs/)
- [Istio Traffic Management](https://istio.io/latest/docs/concepts/traffic-management/)
- [Istio Security](https://istio.io/latest/docs/concepts/security/)
