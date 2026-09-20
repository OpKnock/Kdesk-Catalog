---
type: agent_requested
description: "Manages secrets across platforms with HashiCorp Vault, SOPS, and cloud secret managers: creation, rotation, policies, and injection."
---

# Secret Management

Manages secrets across platforms with HashiCorp Vault, SOPS, and cloud secret managers: creation, rotation, policies, and injection.

## Instructions

# Secret Management

Store, rotate, and inject secrets across Vault, SOPS, and cloud managers.

## What This Skill Does

- Operates Vault KV engines, policies, and tokens
- Encrypts repo files with SOPS (age/KMS/PGP)
- Reads/writes cloud secret manager entries
- Applies least-privilege policies per workload
- Automates rotation workflows

## When to Use

- Choosing a secret storage strategy for an app
- Moving secrets out of env vars and git history
- Rotating credentials safely

## Real Commands

```bash
# Vault
vault secrets enable -path=kv kv-v2
vault kv put kv/app/db password=s3cr3t user=app
vault kv get kv/app/db
vault kv delete kv/app/db
vault policy write app-reader policy.hcl
vault token create -policy=app-reader -ttl=24h
vault kv rotate kv/app/db

# SOPS (age)
sops --encrypt --age $(cat age-public-key) secrets.yaml
sops -e --in-place secrets.yaml
sops -d secrets.yaml
sops --set '["db"]["password"] "newpass"' secrets.yaml

# Cloud
aws secretsmanager put-secret-value --secret-id app/db --secret-string '{"password":"s3cr3t"}'
aws secretsmanager get-secret-value --secret-id app/db --query SecretString --output text
gcloud secrets create db-password --data-file=./pw.txt
```

## Vault Policy

```hcl
path "kv/data/app/db" {
  capabilities = ["read"]
}
```

## Best Practices

- Never store plaintext secrets in git; use SOPS or SealedSecrets
- Use Vault short-TTL tokens and approle auth for services
- Rotate on a schedule; verify rotation with versioning
- Keep KMS/age keys in hardware or isolated credential stores
- Audit access: cloud managers and Vault both log reads

## Capabilities

### vault-operations
Enable engines, write/read secrets, and manage policies and tokens.

**Commands:**
- `vault secrets enable -path=kv kv-v2`
- `vault kv put kv/app/db password=s3cr3t user=app`
- `vault kv get kv/app/db`
- `vault policy write app-reader policy.hcl`
- `vault token create -policy=app-reader -ttl=24h`
- `vault kv rotate kv/app/db`

**Examples:**
- vault kv put kv/app/db password=s3cr3t
- vault kv get kv/app/db
- vault policy write app-reader policy.hcl

### sops-and-cloud
Encrypt files with SOPS and manage cloud secret manager entries.

**Commands:**
- `sops --encrypt --age $(cat ~/.config/sops/age/keys.txt | head -1) secrets.yaml`
- `sops -e --in-place secrets.yaml`
- `sops -d secrets.yaml`
- `aws secretsmanager put-secret-value --secret-id app/db --secret-string '{"password":"s3cr3t"}'`
- `aws secretsmanager get-secret-value --secret-id app/db --query SecretString --output text`
- `gcloud secrets create db-password --data-file=./pw.txt`

**Examples:**
- sops -e --in-place secrets.yaml
- aws secretsmanager get-secret-value --secret-id app/db
- gcloud secrets create db-password --data-file=./pw.txt