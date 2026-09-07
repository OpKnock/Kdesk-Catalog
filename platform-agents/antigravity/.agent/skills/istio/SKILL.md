---
name: "istio"
description: "Installs and operates Istio service mesh: sidecar injection, VirtualService/DestinationRule traffic routing, mTLS, and traffic observation. Use when working with install and verify, traffic management, devops or when the user mentions install and verify, traffic management, devops."
license: "MIT"
compatibility: "Requires istioctl, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(istioctl:*) Bash(kubectl:*)"
---

Installs and operates Istio service mesh: sidecar injection, VirtualService/DestinationRule traffic routing, mTLS, and traffic observation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `istioctl install --set profile=demo`, `kubectl apply -f virtualservice.yaml`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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
