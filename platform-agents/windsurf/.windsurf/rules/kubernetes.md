---
trigger: glob
description: "Architects Kubernetes clusters end-to-end: cluster creation with kind/k3s, RBAC, namespaces, quotas, and multi-cluster access."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# kubernetes

Architects Kubernetes clusters end-to-end: cluster creation with kind/k3s, RBAC, namespaces, quotas, and multi-cluster access.

## Instructions

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
