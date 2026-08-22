---
name: "Kubectl"
description: "Core kubectl operations: resource CRUD, labels/annotations, explain, apply vs create, JSON output, and kubeconfig management."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Kubectl

Core kubectl operations: resource CRUD, labels/annotations, explain, apply vs create, JSON output, and kubeconfig management.

## Instructions

# kubectl Core Operations

Daily Kubernetes CLI work: inspect, create, label, and manage resources.

## What This Skill Does

- Gets resources in wide/JSON/YAML output
- Applies declarative manifests and creates imperative resources
- Edits live resources and deletes with graceful termination
- Manages labels, annotations, and selectors
- Switches contexts and checks RBAC permissions

## When to Use

- Any Kubernetes inspection or change
- Building scripting pipelines over cluster state
- Teaching the core command surface

## Real Commands

```bash
# Inspect
kubectl get pods -A -o wide
kubectl get all -n app
kubectl get deployment web -o yaml
kubectl get pod web-7d9f8c9d4-xk2pq -o jsonpath='{.status.phase}'
kubectl get events -n app --sort-by=.lastTimestamp

# Create / apply / delete
kubectl apply -f deployment.yaml
kubectl create configmap app-config --from-file=config/
kubectl create secret generic db-pass --from-literal=password=s3cr3t
kubectl edit deployment web
kubectl delete pod web-7d9f8c9d4-xk2pq --grace-period=5

# Labels / metadata
kubectl label pod web env=prod --overwrite
kubectl get pods -l app=web,env=prod
kubectl annotate deploy/web kubernetes.io/change-cause="bump image"
kubectl explain deployment.spec.strategy

# Contexts and auth
kubectl config get-contexts
kubectl config use-context prod-east
kubectl auth can-i create deployments -n app
```

## Best Practices

- Prefer `kubectl apply -f` (declarative) over `kubectl create` for repeatable work
- Use `-o wide` for node/IP info, `-o yaml` for full state
- Namespace-scope everything to avoid accidental cluster-wide damage
- Verify RBAC with `kubectl auth can-i` before running privileged operations
- Use `--dry-run=client -o yaml` to preview generated resources

## Capabilities

### resource-operations
Create, get, describe, edit, and delete Kubernetes resources.

**Commands:**
- `kubectl get pods -A -o wide`
- `kubectl apply -f deployment.yaml`
- `kubectl create configmap app-config --from-file=config/`
- `kubectl edit deployment web`
- `kubectl delete pod web-7d9f8c9d4-xk2pq --grace-period=5`
- `kubectl get all -n app`

**Examples:**
- kubectl apply -f deployment.yaml
- kubectl create configmap app-config --from-file=config/
- kubectl get pods -A -o wide

### label-and-metadata
Manage labels, annotations, selectors, and explain resource schema.

**Commands:**
- `kubectl label pod web env=prod`
- `kubectl annotate deploy/web kubernetes.io/change-cause="bump image"`
- `kubectl get pods -l app=web,env=prod`
- `kubectl explain deployment.spec.strategy`
- `kubectl get pod web-7d9f8c9d4-xk2pq -o jsonpath='{.status.phase}'`

**Examples:**
- kubectl get pods -l app=web,env=prod
- kubectl explain deployment.spec.strategy
- kubectl get pod web-7d9f8c9d4-xk2pq -o jsonpath='{.status.phase}'

### kubeconfig-and-context
Switch clusters, inspect contexts, and verify permissions.

**Commands:**
- `kubectl config get-contexts`
- `kubectl config use-context prod-east`
- `kubectl config current-context`
- `kubectl auth can-i create deployments -n app`
- `kubectl api-resources --namespaced=true`

**Examples:**
- kubectl config use-context prod-east
- kubectl auth can-i create deployments
- kubectl config get-contexts