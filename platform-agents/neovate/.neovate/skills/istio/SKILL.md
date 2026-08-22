---
name: "istio"
description: "Installs and operates Istio service mesh: sidecar injection, VirtualService/DestinationRule traffic routing, mTLS, and traffic observation."
---

# istio

Installs and operates Istio service mesh: sidecar injection, VirtualService/DestinationRule traffic routing, mTLS, and traffic observation.

## Instructions

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
