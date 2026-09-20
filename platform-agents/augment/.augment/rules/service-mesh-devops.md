---
type: agent_requested
description: "Evaluates and operates service meshes (Istio, Linkerd, Consul): proxies, sidecar injection, mTLS, mesh observability, and L7 policies."
---

# Service Mesh

Evaluates and operates service meshes (Istio, Linkerd, Consul): proxies, sidecar injection, mTLS, mesh observability, and L7 policies.

## Instructions

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