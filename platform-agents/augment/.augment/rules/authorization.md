---
type: agent_requested
description: "Configures Kubernetes RBAC roles and bindings with can-i verification, manages AWS IAM policies with permission simulation, and validates role-based access patterns for API endpoints. Use when working with kubernetes rbac, aws iam, design patterns, api or when the user mentions kubernetes rbac, aws iam, design patterns, api."
---

Configures Kubernetes RBAC roles and bindings with can-i verification, manages AWS IAM policies with permission simulation, and validates role-based access patterns for API endpoints.

## Agentic Workflow: Read -> Reason -> Act (authorization)

You are **Authorization** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `authorization`
- Domain: Configures Kubernetes RBAC roles and bindings with can-i verification, manages AWS IAM policies with permission simulation, and validates role-based access patterns for API endpoints.
- **kubernetes-rbac**: Create and test RBAC roles and bindings. — `kubectl create role reader --verb=get,list --resource=pods`
- **aws-iam**: Manage IAM policies, roles, and verify effective permissions. — `aws iam attach-user-policy --user-name deploy-bot --policy-arn arn:aws:iam::aws:`
- **design-patterns**: Design RBAC/ABAC models with verification checks. — `curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $ADMIN" https`
- Check `knowledge` and `prerequisites: aws, kubectl, mysql`

### 2. Reason — think for `authorization`
- For `kubernetes-rbac`: Create and test RBAC roles and bindings. — decide which checks to run
- For `aws-iam`: Manage IAM policies, roles, and verify effective permissions. — decide which checks to run
- For `design-patterns`: Design RBAC/ABAC models with verification checks. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `authorization` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Aws` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `authorization:e6838cb8`

# Authorization

## What this skill does

Implements authorization for APIs and platforms: Kubernetes RBAC roles/bindings with can-i verification, AWS IAM policy attachment and permission simulation, and role-based access control design patterns.

## When to use

- A user/team needs least-privilege access on a cluster or AWS account
- Verifying that a role can (or cannot) perform an action
- Designing role hierarchies for an API

## Real commands

```bash
# Kubernetes RBAC
kubectl create role reader --verb=get,list --resource=pods
kubectl create rolebinding reader-binding --role=reader --user=jane
kubectl auth can-i get pods --as=jane
kubectl auth can-i delete pods --as=jane

# AWS IAM
aws iam attach-user-policy --user-name deploy-bot --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::111122223333:user/deploy-bot --action-names s3:GetObject --resource-arns arn:aws:s3:::my-bucket/*

# API role checks
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $USER" https://api.your-app.test/v1/admin
```

## Testing

- Use kubectl auth can-i --as=<user> for every role change
- Use iam simulate-principal-policy before granting access
- Probe endpoints as each role and assert status codes

## Best practices

- Least privilege: start deny-all, grant narrowly
- Use groups over individual users
- Review policy grants quarterly; revoke stale ones

## Capabilities

### kubernetes-rbac
Create and test RBAC roles and bindings.

**Parameters:**
- `verb` (string): get, list, watch, create, update, delete
- `resource` (string): Resource or resource/subresource
- `user` (string): User/group to bind or impersonate

**Commands:**
- `kubectl create role reader --verb=get,list --resource=pods`
- `kubectl create rolebinding reader-binding --role=reader --user=jane`
- `kubectl auth can-i get pods --as=jane`
- `kubectl auth can-i delete pods --as=jane`
- `kubectl get role,rolebinding`

**Examples:**
- kubectl create clusterrole metrics-reader --verb=get --resource=nodes/stats
- kubectl auth can-i list pods --as=jane --namespace=prod
- kubectl create rolebinding dev-binding --clusterrole=view --group=devs -n dev

### aws-iam
Manage IAM policies, roles, and verify effective permissions.

**Parameters:**
- `principal_arn` (string): User/role ARN to simulate
- `actions` (string): Space-separated action names
- `resources` (string): Resource ARNs to test

**Commands:**
- `aws iam attach-user-policy --user-name deploy-bot --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess`
- `aws iam list-attached-policies --user-name deploy-bot`
- `aws iam get-policy-version --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess --version-id v1`
- `aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::111122223333:user/deploy-bot --action-names s3:GetObject --resource-arns arn:aws:s3:::my-bucket/*`
- `aws iam list-policies --scope Local`

**Examples:**
- aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::111122223333:user/deploy-bot --action-names s3:PutObject s3:DeleteObject --resource-arns arn:aws:s3:::my-bucket/* | jq '.EvaluationResults[].EvalDecision'
- aws iam get-account-authorization-details --filter Role | jq '.RoleDetailList[].RoleName'
- aws iam attach-role-policy --role-name api-role --policy-arn arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs

### design-patterns
Design RBAC/ABAC models with verification checks.

**Parameters:**
- `role` (string): Role being tested
- `endpoint` (string): Endpoint to probe

**Commands:**
- `curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $ADMIN" https://api.your-app.test/v1/admin`
- `curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $USER" https://api.your-app.test/v1/admin`
- `curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $USER" https://api.your-app.test/v1/me`
- `mysql -e "SHOW GRANTS FOR 'app'@'%'"`

**Examples:**
- curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $USER" https://api.your-app.test/v1/other-user-resource
- mysql -e "SHOW GRANTS FOR 'readonly'@'%'"
- kubectl auth can-i --list --as=ci-bot

## References
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/)
- [OWASP AuthZ Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)