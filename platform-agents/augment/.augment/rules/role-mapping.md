---
type: agent_requested
description: "Expert role mapping skill covering Kubernetes RBAC bindings, kubectl auth checks, and AWS IAM role/policy inspection to trace who can do what."
---

# Role Mapping

Expert role mapping skill covering Kubernetes RBAC bindings, kubectl auth checks, and AWS IAM role/policy inspection to trace who can do what.

## Instructions

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