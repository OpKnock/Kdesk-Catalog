---
name: "service-mesh-devops"
description: "Evaluates and operates service meshes (Istio, Linkerd, Consul): proxies, sidecar injection, mTLS, mesh observability, and L7 policies. Use when working with mesh selection and install, traffic and security policies, devops or when the user mentions mesh selection and install, traffic and security policies, devops."
license: "MIT"
compatibility: "Requires consul, helm, istioctl, kubectl, linkerd. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(consul:*) Bash(helm:*) Bash(istioctl:*) Bash(kubectl:*) Bash(linkerd:*)"
---

Evaluates and operates service meshes (Istio, Linkerd, Consul): proxies, sidecar injection, mTLS, mesh observability, and L7 policies.

## Agentic Workflow: Read -> Reason -> Act (service-mesh-devops)

You are **Service Mesh** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `service-mesh-devops`
- Domain: Evaluates and operates service meshes (Istio, Linkerd, Consul): proxies, sidecar injection, mTLS, mesh observability, and L7 policies.
- **mesh-selection-and-install**: Choose and install a mesh (Istio/Linkerd/Consul) for a workload profile. — `istioctl install --set profile=default -y`
- **traffic-and-security-policies**: Enforce mTLS, AuthorizationPolicies, and L7 routing rules. — `kubectl apply -f peerauthentication.yaml`
- Check `knowledge` and `prerequisites: consul, helm, istioctl, kubectl`

### 2. Reason — think for `service-mesh-devops`
- For `mesh-selection-and-install`: Choose and install a mesh (Istio/Linkerd/Consul) for a workload profile. — decide which checks to run
- For `traffic-and-security-policies`: Enforce mTLS, AuthorizationPolicies, and L7 routing rules. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `service-mesh-devops` tools
- Tools: `Glob`, `Grep`, `Read`, `Istioctl`, `Linkerd` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `service-mesh-devops:ac3d8b75`

# Service Mesh Operations

Select, install, and operate service meshes for mTLS, routing, and observability.

## What This Skill Does

- Compares Istio vs Linkerd vs Consul for workload profiles
- Installs control planes and injects sidecar proxies
- Enforces mTLS and authorization policies
- Configures L7 traffic rules (canaries, timeouts, retries)
- Observes proxy-level traffic (tap, proxy-config)

## When to Use

- Adding mTLS across a fleet without app changes
- Fine-grained east-west traffic policies
- Mesh observability: per-service success/latency

## Real Commands

```bash
# Istio
istioctl install --set profile=default -y
istioctl verify-install
kubectl label ns app istio-injection=enabled
kubectl apply -f peerauthentication.yaml
istioctl proxy-status
istioctl proxy-config secret web-xyz-abc

# Linkerd
linkerd check --pre
linkerd install | kubectl apply -f -
linkerd check
linkerd inject deploy.yaml | kubectl apply -f -
linkerd tap deploy/web -n app
linkerd stat deploy -n app

# Consul
helm install consul hashicorp/consul -n consul --create-namespace
consul members
consul intention create web api --allow
consul catalog services
```

## Selection Guide

- Linkerd: minimal overhead, simple, great default for mTLS + metrics
- Istio: richest L7 policy and traffic management (canary, fault injection)
- Consul: mesh + service discovery + multi-datacenter

## Best Practices

- Start with mTLS STRICT after verifying all workloads have proxies
- Test policies in a canary namespace first
- Watch control plane health (proxy-status, linkerd check)
- Size control planes for node/proxy count; avoid oversubscription
- Keep mesh version upgrades on the same cadence as clusters

## Capabilities

### mesh-selection-and-install
Choose and install a mesh (Istio/Linkerd/Consul) for a workload profile.

**Parameters:**
- `mesh` (string): Mesh to install: istio, linkerd, consul
- `namespace` (string): Mesh namespace

**Commands:**
- `istioctl install --set profile=default -y`
- `linkerd check --pre`
- `linkerd install | kubectl apply -f -`
- `helm install consul hashicorp/consul --set global.name=consul -n consul`
- `consul members`
- `istioctl verify-install`

**Examples:**
- istioctl install --set profile=default -y
- linkerd install | kubectl apply -f -
- helm install consul hashicorp/consul -n consul

### traffic-and-security-policies
Enforce mTLS, AuthorizationPolicies, and L7 routing rules.

**Parameters:**
- `pod` (string): Pod for proxy inspection
- `manifest` (string): Policy CR file

**Commands:**
- `kubectl apply -f peerauthentication.yaml`
- `kubectl apply -f authorizationpolicy.yaml`
- `kubectl apply -f virtualservice.yaml`
- `linkerd tap deploy/web -n app`
- `istioctl proxy-config secret demo-pod`
- `consul intention create web api --allow`

**Examples:**
- kubectl apply -f peerauthentication.yaml
- linkerd tap deploy/web -n app
- consul intention create web api --allow

## References
- [Istio Concepts](https://istio.io/latest/docs/concepts/)
- [Linkerd Overview](https://linkerd.io/2.15/overview/)
- [Consul Service Mesh](https://developer.hashicorp.com/consul/docs/connect)
