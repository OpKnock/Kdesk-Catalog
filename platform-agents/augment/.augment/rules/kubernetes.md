---
type: agent_requested
description: "Architects Kubernetes clusters end-to-end: cluster creation with kind/k3s, RBAC, namespaces, quotas, and multi-cluster access. Use when working with cluster creation, rbac and quotas, devops or when the user mentions cluster creation, rbac and quotas, devops."
---

Architects Kubernetes clusters end-to-end: cluster creation with kind/k3s, RBAC, namespaces, quotas, and multi-cluster access.

## Agentic Workflow: Read -> Reason -> Act (kubernetes)

You are **kubernetes** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `kubernetes`
- Domain: Architects Kubernetes clusters end-to-end: cluster creation with kind/k3s, RBAC, namespaces, quotas, and multi-cluster access.
- **cluster-creation**: Create local and production-style clusters with kind, k3s, and kubeadm. — `kind create cluster --name dev --config kind-config.yaml`
- **rbac-and-quotas**: Configure namespaces, RBAC, quotas, and limits. — `kubectl create namespace staging`
- Check `knowledge` and `prerequisites: k3s, kind, kubeadm, kubectl`

### 2. Reason — think for `kubernetes`
- For `cluster-creation`: Create local and production-style clusters with kind, k3s, and kubeadm. — decide which checks to run
- For `rbac-and-quotas`: Configure namespaces, RBAC, quotas, and limits. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kubernetes` tools
- Tools: `Glob`, `Grep`, `Read`, `Kind`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kubernetes:e442fbf0`

# Kubernetes Platform Engineering

Design, create, and govern Kubernetes clusters: from local kind to production control planes.

## What This Skill Does

- Creates clusters (kind, k3s, kubeadm) with repeatable configs
- Configures namespaces, RBAC, quotas, and limit ranges
- Manages multi-cluster access via kubeconfig contexts
- Sets up CNI, ingress, and storage foundations
- Audits access with kubectl auth can-i

## When to Use

- Standing up dev/test clusters locally
- Bootstrapping a production control plane with kubeadm
- Building multi-tenant namespaces with quotas and RBAC

## Real Commands

```bash
# Local clusters
kind create cluster --name dev --config kind-config.yaml
kind get clusters
kind delete cluster --name dev
curl -sfL https://get.k3s.io | sh -
k3s kubectl get nodes

# Production-style
kubeadm init --pod-network-cidr=10.244.0.0/16
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# Tenancy
kubectl create namespace staging
kubectl create serviceaccount ci-bot -n staging
kubectl create rolebinding ci-bot-binding --role=edit --serviceaccount=staging:ci-bot -n staging
kubectl apply -f resourcequota.yaml
kubectl auth can-i list pods --as=system:serviceaccount:staging:ci-bot
```

## ResourceQuota Example

```yaml
apiVersion: v1
kind: ResourceQuota
metadata: { name: staging-quota, namespace: staging }
spec:
  hard:
    requests.cpu: "8"
    requests.memory: 16Gi
    limits.cpu: "16"
    limits.memory: 32Gi
    count/pods: "100"
```

## Best Practices

- Version cluster configs (kind-config, kubeadm.yaml) in git
- Separate namespaces per team with quotas to prevent noisy-neighbor
- Least-privilege RBAC: default deny, explicit allow
- Test RBAC with --as impersonation before granting
- Use kubectl auth can-i in CI to verify permissions

## Capabilities

### cluster-creation
Create local and production-style clusters with kind, k3s, and kubeadm.

**Parameters:**
- `cluster-name` (string): Cluster name
- `config` (string): Kind cluster config file

**Commands:**
- `kind create cluster --name dev --config kind-config.yaml`
- `kind get clusters`
- `curl -sfL https://get.k3s.io | sh -`
- `k3s kubectl get nodes`
- `kubeadm init --pod-network-cidr=10.244.0.0/16`
- `kind delete cluster --name dev`

**Examples:**
- kind create cluster --name dev --config kind-config.yaml
- curl -sfL https://get.k3s.io | sh -
- kubeadm init --pod-network-cidr=10.244.0.0/16

### rbac-and-quotas
Configure namespaces, RBAC, quotas, and limits.

**Parameters:**
- `namespace` (string): Namespace name
- `serviceaccount` (string): Service account name

**Commands:**
- `kubectl create namespace staging`
- `kubectl create serviceaccount ci-bot -n staging`
- `kubectl create rolebinding ci-bot-binding --role=edit --serviceaccount=staging:ci-bot -n staging`
- `kubectl apply -f resourcequota.yaml`
- `kubectl apply -f limitrange.yaml`
- `kubectl get quotas,limits -n staging`

**Examples:**
- kubectl create rolebinding ci-bot-binding --role=edit --serviceaccount=staging:ci-bot -n staging
- kubectl apply -f resourcequota.yaml
- kubectl auth can-i list pods --as=system:serviceaccount:staging:ci-bot

## References
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kind](https://kind.sigs.k8s.io/)
- [K3s](https://docs.k3s.io/)
- [RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)