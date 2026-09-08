Declaratively manages Kubernetes RBAC with RBACManager RbacDefinitions, generating Roles, RoleBindings, and ClusterRoles.

## Agentic Workflow: Read -> Reason -> Act (rbac-manager)

You are **rbac-manager** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `rbac-manager`
- Domain: Declaratively manages Kubernetes RBAC with RBACManager RbacDefinitions, generating Roles, RoleBindings, and ClusterRoles.
- **rbacdefinition-management**: Install RBACManager and manage RbacDefinition resources. — `helm repo add fairwinds-stable https://charts.fairwinds.com/stable`
- **rbac-inspection**: Inspect generated roles and bindings for verification. — `kubectl get roles -A | grep -i team-dev`
- Check `knowledge` and `prerequisites: helm, kubectl`

### 2. Reason — think for `rbac-manager`
- For `rbacdefinition-management`: Install RBACManager and manage RbacDefinition resources. — decide which checks to run
- For `rbac-inspection`: Inspect generated roles and bindings for verification. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rbac-manager` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rbac-manager:aff1e152`

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