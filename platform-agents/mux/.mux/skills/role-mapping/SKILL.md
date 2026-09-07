---
name: "role-mapping"
description: "Expert role mapping skill covering Kubernetes RBAC bindings, kubectl auth checks, and AWS IAM role/policy inspection to trace who can do what. Use when working with rbac iam mapping, api or when the user mentions rbac iam mapping, api."
license: "MIT"
compatibility: "Requires aws, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(aws:*) Bash(kubectl:*)"
---

Expert role mapping skill covering Kubernetes RBAC bindings, kubectl auth checks, and AWS IAM role/policy inspection to trace who can do what.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl get rolebindings -A -o wide`
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

# Role Mapping

Expert skill for mapping users to roles across Kubernetes RBAC and AWS IAM.

## What this skill does

- Lists role and clusterrole bindings to see who has which role
- Checks effective permissions with kubectl auth can-i
- Inspects AWS IAM roles and their attached policies

## When to use

- Auditing who can deploy to a namespace after an incident
- Removing stale permissions during an offboarding
- Verifying least-privilege for CI service accounts

## Real commands

```bash
# All role bindings cluster-wide
kubectl get rolebindings -A -o wide

# What can the current user do in a namespace?
kubectl auth can-i --list -n backend
kubectl auth can-i create deployments -n backend

# Cluster-level bindings
kubectl get clusterrolebinding -A -o wide | head -20

# AWS IAM roles and their policies
aws iam list-roles --query 'Roles[].RoleName' --output table
aws iam list-attached-role-policies --role-name app-prod-role --output table
aws iam list-role-policies --role-name app-prod-role
```

## Mapping workflow

1. Find the subject: kubectl get rolebindings -n backend -o yaml
2. Check effective access: kubectl auth can-i --list -n backend
3. For cloud roles: list IAM policies and the trust policy

## Testing

```bash
kubectl auth can-i delete secrets -n backend   # should be no for CI accounts
```

## Best practices

- Prefer namespaced Roles over ClusterRoles where possible
- Re-audit bindings after every team change
- Use aws iam simulate-principal-policy to test role access before granting

## Capabilities

### rbac-iam-mapping
Map users to roles in Kubernetes RBAC and AWS IAM

**Parameters:**
- `namespace` (string): Namespace to scope RBAC queries
- `role_name` (string): AWS IAM role name
- `verb_resource` (string): Check like create deployments

**Commands:**
- `kubectl get rolebindings -A -o wide`
- `kubectl auth can-i --list -n backend`
- `kubectl get clusterrolebinding -A -o wide | head -20`
- `aws iam list-roles --query 'Roles[].RoleName' --output table`
- `aws iam list-attached-role-policies --role-name app-prod-role --output table`

**Examples:**
- kubectl auth can-i create deployments -n backend
- kubectl get rolebindings -n backend -o yaml
- aws iam list-role-policies --role-name app-prod-role

## References
- [K8s RBAC reference](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [AWS IAM roles docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
