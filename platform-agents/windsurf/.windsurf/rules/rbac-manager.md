---
trigger: glob
description: "Declaratively manages Kubernetes RBAC with RBACManager RbacDefinitions, generating Roles, RoleBindings, and ClusterRoles. Use when working with rbacdefinition management, rbac inspection, security or when the user mentions rbacdefinition management, rbac inspection, security."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Declaratively manages Kubernetes RBAC with RBACManager RbacDefinitions, generating Roles, RoleBindings, and ClusterRoles.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `helm repo add fairwinds-stable https://charts.fairwinds.com/`, `kubectl get roles -A | grep -i team-dev`
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

**Parameters:**
- `name` (string): RbacDefinition name
- `namespace` (string): Operator namespace

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

**Parameters:**
- `serviceAccount` (string): SA identity for auth can-i checks
- `namespace` (string): Namespace scope for RBAC and auth can-i checks.

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

## References
- [RBAC Manager Documentation](https://rbac-manager.docs.fairwinds.com/)
- [Fairwinds RBAC Manager GitHub](https://github.com/FairwindsOps/rbac-manager)
