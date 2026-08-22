---
type: agent_requested
description: "Manages the complete secret lifecycle across Kubernetes, SOPS-encrypted files, HashiCorp Vault, and AWS Secrets Manager. Handles creation, rotation, and access patterns for production credentials without exposing plaintext in repositories or container images."
---

# Secrets Management

Manages the complete secret lifecycle across Kubernetes, SOPS-encrypted files, HashiCorp Vault, and AWS Secrets Manager. Handles creation, rotation, and access patterns for production credentials without exposing plaintext in repositories or container images.

## Instructions

# Secrets Management

Manages the complete secret lifecycle across Kubernetes, SOPS-encrypted files, HashiCorp Vault, and AWS Secrets Manager.

## What this skill does

- Creates and reads Kubernetes Secrets from files and literals
- Encrypts config files in git with SOPS using age, PGP, or KMS
- Stores and retrieves secrets in Vault KV v2 and AWS Secrets Manager
- Rotates credentials without application restarts

## When to use

- Deciding where a new credential should live (k8s, Vault, AWS, or SOPS)
- Rotating database passwords or API keys during an incident
- Migrating from environment variables to a proper secret store
- Storing encrypted configuration in GitOps repositories

## Real commands

```bash
# Kubernetes: create and read secrets
kubectl create secret generic api --from-file=config.json --from-literal=API_KEY=xxx
kubectl get secret api -o jsonpath='{.data.API_KEY}' | base64 -d

# SOPS: encrypt/decrypt a config file in place
sops --encrypt --in-place secrets/application.yaml
sops --decrypt secrets/application.yaml

# Vault KV v2: write and read versioned secrets
vault kv put secret/payments apikey=sk_live_123
vault kv get secret/payments

# AWS Secrets Manager: retrieve secret value
aws secretsmanager get-secret-value --secret-id payments/api --query SecretString --output text
```

## Rotation pattern

```bash
# New value in, old value retired
vault kv put secret/payments apikey=sk_live_456
kubectl rollout restart deployment/api
```

## Testing

```bash
sops --decrypt secrets/application.yaml | yq '.database.password'
vault kv get secret/payments
```

## Best practices

- Kubernetes Secrets alone are base64, not encryption: use Sealed Secrets or external stores
- Rotate on a schedule, not only after leaks
- Audit access: Vault audit logs, AWS CloudTrail, Kubernetes audit log
- Use SOPS creation rules (`.sops.yaml`) so encryption needs no flags


Hand-crafted skill for managing secrets across Kubernetes, SOPS, Vault, and AWS.


## What this skill does


- Creates and reads Kubernetes Secrets from files and literals

- Encrypts config files in git with SOPS

- Stores and retrieves secrets in Vault and AWS Secrets Manager


## When to use


- Deciding where a new secret should live

- Rotating credentials during an incident

- Migrating from env vars to a real secret store


## Real commands


```bash

# Kubernetes

kubectl create secret generic api --from-file=config.json --from-literal=API_KEY=xxx

kubectl get secret api -o jsonpath=''{.data.API_KEY}'' | base64 -d


# SOPS: encrypt/decrypt a config file in place

sops --encrypt --in-place secrets/application.yaml

sops --decrypt secrets/application.yaml


# Vault (kv v2)

vault kv put secret/payments apikey=sk_live_123

vault kv get secret/payments


# AWS Secrets Manager

aws secretsmanager get-secret-value --secret-id payments/api --query SecretString --output text

```


## Rotation pattern


```bash

# New value in, old value retired

vault kv put secret/payments apikey=sk_live_456

kubectl rollout restart deployment/api

```


## Testing


```bash

sops --decrypt secrets/application.yaml | yq ''.database.password''

vault kv get secret/payments

```


## Best practices


- Kubernetes Secrets alone are base64, not encryption: use a store or Sealed Secrets

- Rotate on a schedule, not only after leaks

- Audit access: Vault audit logs, AWS CloudTrail, k8s audit log

'

## Capabilities

### secrets-lifecycle
Create, read, encrypt, and rotate secrets across stores

**Commands:**
- `kubectl create secret generic api --from-file=config.json --from-literal=API_KEY=xxx`
- `kubectl get secret api -o jsonpath='{.data.API_KEY}' | base64 -d`
- `sops --encrypt --in-place secrets/application.yaml`
- `vault kv put secret/payments apikey=sk_live_123`
- `aws secretsmanager get-secret-value --secret-id payments/api --query SecretString --output text`

**Examples:**
- kubectl create secret generic api --from-literal=API_KEY=xxx
- vault kv get secret/payments
- sops --decrypt secrets/application.yaml