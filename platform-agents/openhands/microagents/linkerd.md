---
name: "linkerd"
description: "Deploys and operates the Linkerd service mesh: install/upgrade, mesh injection, golden-metric stats, tap traffic, and multicluster links."
type: knowledge
triggers: ["linkerd", "install-and-mesh", "observability-and-traffic"]
---

# linkerd

Deploys and operates the Linkerd service mesh: install/upgrade, mesh injection, golden-metric stats, tap traffic, and multicluster links.

## Instructions

# Linkerd Service Mesh

Add a lightweight ultralight mesh: sidecars, mTLS, golden metrics, and live tap.

## What This Skill Does

- Installs the control plane and viz extension
- Injects linkerd-proxy sidecars into workloads
- Views golden metrics (success rate, RPS, latency) per resource
- Taps live traffic with zero instrumentation
- Links clusters with multicluster service mirroring

## When to Use

- mTLS + per-service metrics without complex sidecar tuning
- Debugging latency or error rate on specific routes
- Progressive adoption: mesh a namespace at a time

## Real Commands

```bash
# Install
linkerd check --pre
linkerd install | kubectl apply -f -
linkerd check
kubectl get -n linkerd deploy

# Inject
linkerd inject deployment.yaml | kubectl apply -f -
kubectl rollout restart deployment/web
kubectl get pods -l linkerd.io/proxy=deployment --field-selector=status.phase=Running

# Observability
linkerd viz install | kubectl apply -f -
linkerd stat deploy -n app
linkerd top deploy -n app
linkerd tap deploy/web -n app --to deploy/api
linkerd viz dashboard
```

## Multicluster

```bash
linkerd multicluster install | kubectl apply -f -
linkerd multicluster link --cluster-name=prod
linkerd multicluster gateways
```

## Best Practices

- Run `linkerd check --pre` before install and `linkerd check` after
- Validate proxy injection: pods must show 2 containers
- Use tap only briefly in production (it is live traffic)
- Enable mTLS by default; service-to-service trust is automatic
- Use `linkerd stat --to` to find which dependency has high latency

## Capabilities

### install-and-mesh
Install Linkerd, run preflight checks, and inject sidecars.

**Commands:**
- `linkerd check --pre`
- `linkerd install | kubectl apply -f -`
- `linkerd check`
- `kubectl get -n linkerd deploy`
- `linkerd inject deployment.yaml | kubectl apply -f -`
- `kubectl rollout restart deployment/web`

**Examples:**
- linkerd check --pre
- linkerd install | kubectl apply -f -
- linkerd inject deployment.yaml | kubectl apply -f -

### observability-and-traffic
Inspect service metrics, top talkers, and live traffic with tap.

**Commands:**
- `linkerd viz install | kubectl apply -f -`
- `linkerd stat deploy -n app`
- `linkerd top deploy -n app`
- `linkerd tap deploy/web -n app --to deploy/api`
- `linkerd viz dashboard`
- `linkerd viz profiles -n app`

**Examples:**
- linkerd stat deploy -n app
- linkerd tap deploy/web -n app
- linkerd viz dashboard
