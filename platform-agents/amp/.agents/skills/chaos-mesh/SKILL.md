---
name: "chaos-mesh"
description: "Run Kubernetes chaos experiments with Chaos Mesh: install via helm, apply PodChaos/NetworkChaos, and inspect injection status. Use when working with chaos mesh install, chaos injection, api or when the user mentions chaos mesh install, chaos injection, api."
license: "MIT"
compatibility: "Requires helm, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(helm:*) Bash(kubectl:*)"
---

Run Kubernetes chaos experiments with Chaos Mesh: install via helm, apply PodChaos/NetworkChaos, and inspect injection status.

## Agentic Workflow: Read -> Reason -> Act (chaos-mesh)

You are **Chaos Mesh** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `chaos-mesh`
- Domain: Run Kubernetes chaos experiments with Chaos Mesh: install via helm, apply PodChaos/NetworkChaos, and inspect injection status.
- **chaos-mesh-install**: Install Chaos Mesh CRDs and controller in the cluster — `helm repo add chaos-mesh https://charts.chaos-mesh.org`
- **chaos-injection**: Apply PodChaos and NetworkChaos resources and observe fault injection — `kubectl apply -f pod-kill.yaml`
- Check `knowledge` and `prerequisites: helm, kubectl`

### 2. Reason — think for `chaos-mesh`
- For `chaos-mesh-install`: Install Chaos Mesh CRDs and controller in the cluster — decide which checks to run
- For `chaos-injection`: Apply PodChaos and NetworkChaos resources and observe fault injection — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `chaos-mesh` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `chaos-mesh:b01590f5`

# Chaos Mesh

Run Kubernetes chaos experiments natively with Chaos Mesh.

## When to Use

- Fault injection on pods, network, CPU, memory, and IO
- Declarative chaos as CRDs in git
- Observing service behavior under real faults

## Install

```bash
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh --namespace chaos-mesh --create-namespace
kubectl get pods -n chaos-mesh
```

## PodChaos (Kill)

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill-nginx
  namespace: myapp
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces: [myapp]
    labelSelectors:
      app: nginx
  duration: 30s
```

```bash
kubectl apply -f pod-kill.yaml
kubectl get podchaos -n myapp
kubectl describe podchaos pod-kill-nginx -n myapp
```

## NetworkChaos (Loss)

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-loss
  namespace: myapp
spec:
  action: loss
  mode: all
  selector:
    labelSelectors:
      app: api
  loss:
    loss: "30"
  duration: 30s
```

## Observe and Clean

```bash
kubectl get networkchaos -n myapp
kubectl describe networkchaos network-loss -n myapp
kubectl delete networkchaos --all -n myapp
```

## Testing

```bash
# During the fault, request the API and watch failures
curl -s -o /dev/null -w "%{http_code}\n" http://api.example.com/health
```

## Best Practices

- Target pods with precise labelSelectors
- Use mode: one for small blast radius first
- Always set duration; verify expiration
- Run in staging before production
- Use the dashboard for experiment history
- Combine with alerting to validate observability

## Capabilities

### chaos-mesh-install
Install Chaos Mesh CRDs and controller in the cluster

**Parameters:**
- `namespace` (string): Namespace for Chaos Mesh, default chaos-mesh

**Commands:**
- `helm repo add chaos-mesh https://charts.chaos-mesh.org`
- `helm install chaos-mesh chaos-mesh/chaos-mesh --namespace chaos-mesh --create-namespace`
- `kubectl get pods -n chaos-mesh`
- `kubectl get crd | grep chaos`

**Examples:**
- helm repo add chaos-mesh https://charts.chaos-mesh.org && helm install chaos-mesh chaos-mesh/chaos-mesh --namespace chaos-mesh --create-namespace
- kubectl get pods -n chaos-mesh -w
- kubectl get crd | grep chaos

### chaos-injection
Apply PodChaos and NetworkChaos resources and observe fault injection

**Parameters:**
- `chaos_kind` (string): podchaos, networkchaos, stresschaos, or iochaos
- `manifest` (string): Path to chaos YAML manifest

**Commands:**
- `kubectl apply -f pod-kill.yaml`
- `kubectl get podchaos -n myapp`
- `kubectl get networkchaos -n myapp`
- `kubectl describe podchaos pod-kill-nginx -n myapp`

**Examples:**
- kubectl apply -f pod-kill.yaml && kubectl get podchaos -n myapp
- kubectl apply -f network-loss.yaml && kubectl get networkchaos -n myapp
- kubectl describe networkchaos network-loss -n myapp

## References
- [Chaos Mesh Docs](https://chaos-mesh.org/docs/)
- [Chaos Mesh Dashboard](https://chaos-mesh.org/docs/basic-features/dashboard/)
