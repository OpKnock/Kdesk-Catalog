---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# rbac-manager

Declaratively manages Kubernetes RBAC with RBACManager RbacDefinitions, generating Roles, RoleBindings, and ClusterRoles.

## Instructions

# RBAC Manager

Declarative Kubernetes RBAC with RbacDefinitions.

## What This Skill Does

- Installs the RBAC Manager operator
- Defines per-team RbacDefinitions with rules and subject matchers
- Generates and reconciles Roles, RoleBindings, and ClusterRoles
- Inspects the resulting bindings and effective permissions

## When to Use

- Managing team namespaces with self-service access
- Enforcing least-privilege service accounts at scale
- Auditing who can do what across clusters

## Real Commands

```bash
# Install
helm repo add fairwinds-stable https://charts.fairwinds.com/stable
helm install rbac-manager fairwinds-stable/rbac-manager -n rbac-manager --create-namespace

# Define and apply
kubectl apply -f rbacdefinition.yaml
kubectl get rbacdefinitions.rbacmanager.reactiveops.io -A
kubectl describe rbacdefinition team-dev

# Verify generated RBAC
kubectl get rolebindings.rbacmanager.reactiveops.io -A
kubectl get clusterrolebindings.rbacmanager.reactiveops.io
kubectl auth can-i create deployments --as=system:serviceaccount:dev:team-dev
```

## Sample RbacDefinition

```yaml
apiVersion: rbacmanager.reactiveops.io/v1beta1
kind: RbacDefinition
metadata:
  name: team-dev
spec:
  rbacBindings:
    - name: team-dev-edit
      subjects:
        - kind: User
          name: alice@example.com
      clusterRole: edit
      clusterWide: false
      namespaces:
        - dev
```

## Best Practices

- Scope bindings with clusterWide: false unless truly needed
- Model access by team, not by individual ad-hoc edits
- Verify with kubectl auth can-i, not by assumption
- Review generated resources in dry-run gitops diffs
- Rotate subject matchers carefully: they trigger wide regeneration

## Capabilities

### rbacdefinition-management
Install RBACManager and manage RbacDefinition resources.

**Commands:**
- `helm repo add fairwinds-stable https://charts.fairwinds.com/stable`
- `helm install rbac-manager fairwinds-stable/rbac-manager -n rbac-manager --create-namespace`
- `kubectl get rbacdefinitions.rbacmanager.reactiveops.io -A`
- `kubectl apply -f rbacdefinition.yaml`
- `kubectl describe rbacdefinition team-dev`

**Examples:**
- helm install rbac-manager fairwinds-stable/rbac-manager
- kubectl get rbacdefinitions.rbacmanager.reactiveops.io -A
- kubectl apply -f rbacdefinition.yaml

### rbac-inspection
Inspect generated roles and bindings for verification.

**Commands:**
- `kubectl get roles -A | grep -i team-dev`
- `kubectl get rolebindings.rbacmanager.reactiveops.io -A`
- `kubectl get clusterrolebindings.rbacmanager.reactiveops.io`
- `kubectl auth can-i --list --as=system:serviceaccount:default:team-dev`
- `kubectl get clusterroles | grep rbac-manager`

**Examples:**
- kubectl get rolebindings.rbacmanager.reactiveops.io -A
- kubectl auth can-i create deployments --as=system:serviceaccount:prod:deployer
- kubectl get clusterroles | grep team
