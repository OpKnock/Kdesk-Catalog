---
applyTo: "**/*.go **/*.r **/*.rs **/*.sh **/*.{yaml,yml}"
---

Deploys and operates the Linkerd service mesh: install/upgrade, mesh injection, golden-metric stats, tap traffic, and multicluster links.

## Agentic Workflow: Read -> Reason -> Act (linkerd)

You are **linkerd** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `linkerd`
- Domain: Deploys and operates the Linkerd service mesh: install/upgrade, mesh injection, golden-metric stats, tap traffic, and multicluster links.
- **install-and-mesh**: Install Linkerd, run preflight checks, and inject sidecars. — `linkerd check --pre`
- **observability-and-traffic**: Inspect service metrics, top talkers, and live traffic with tap. — `linkerd viz install | kubectl apply -f -`
- Check `knowledge` and `prerequisites: kubectl, linkerd`

### 2. Reason — think for `linkerd`
- For `install-and-mesh`: Install Linkerd, run preflight checks, and inject sidecars. — decide which checks to run
- For `observability-and-traffic`: Inspect service metrics, top talkers, and live traffic with tap. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `linkerd` tools
- Tools: `Glob`, `Grep`, `Read`, `Linkerd`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `linkerd:1a6ff93d`

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

**Parameters:**
- `manifest` (string): Manifest to inject sidecars into
- `namespace` (string): Namespace to mesh/inject

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

**Parameters:**
- `namespace` (string): Namespace to observe
- `resource` (string): Resource for stats, e.g. deploy/web

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

## References
- [Linkerd Documentation](https://linkerd.io/2.15/overview/)
- [Linkerd CLI](https://linkerd.io/2.15/reference/cli/)
- [Linkerd Multicluster](https://linkerd.io/2.15/features/multicluster/)
