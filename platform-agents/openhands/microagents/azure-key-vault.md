---
name: "azure-key-vault"
description: "Centralizes credentials and cryptographic material in a managed HSM-backed store using the Azure CLI: provisions vault instances, performs secret CRUD with versioning and expiry, manages asymmetric keys, and configures access policies or RBAC for service identities."
type: knowledge
triggers: ["azure-key-vault", "vault-lifecycle", "secrets", "keys-access"]
---

# Azure Key Vault

Centralizes credentials and cryptographic material in a managed HSM-backed store using the Azure CLI: provisions vault instances, performs secret CRUD with versioning and expiry, manages asymmetric keys, and configures access policies or RBAC for service identities.

## Instructions

# Azure Key Vault

## What this skill does

Centralizes secrets, keys, and certificates in Azure Key Vault using the Azure CLI: provisions vaults, performs secret CRUD with versioning and expiry, manages cryptographic keys, and configures access policies or RBAC for service identities.

## When to use

- Centralizing secrets instead of .env files
- Storing encryption keys for a service
- Rotating credentials with versioned secrets

## Real commands

```bash
# Create a vault
az keyvault create --name mykv --resource-group rg

# Set and read a secret
az keyvault secret set --vault-name mykv --name db-password --value secret123
az keyvault secret show --vault-name mykv --name db-password --query 'value' -o tsv

# Versioned rotation
az keyvault secret set --vault-name mykv --name api-key --value $(openssl rand -hex 32)

# Keys
az keyvault key create --vault-name mykv --name rsa-key --protection software

# Access policy
az keyvault set-policy --vault-name mykv --object-id a1b2c3d4-e5f6-7890-abcd-ef1234567890 --secret-permissions get list set delete
```

## Testing

- Verify identity access with a managed identity + curl to the vault URI
- List secret versions to confirm rotation creates versions

## Best practices

- Use managed identities over service principals where possible
- Set expiry dates on secrets and rotate proactively
- Restrict network access with vault firewall rules
- Log access via diagnostic settings to a Log Analytics workspace

## Capabilities

### vault-lifecycle
Create and manage Key Vault instances.

**Commands:**
- `az keyvault create --name mykv --resource-group rg`
- `az keyvault show --name mykv`
- `az keyvault list --resource-group rg`
- `az keyvault delete --name mykv`
- `az keyvault purge --name mykv`

**Examples:**
- az keyvault create --name mykv --resource-group rg --location eastus
- az keyvault list --resource-group rg --query '[].{name:name,uri:properties.vaultUri}' -o table
- az keyvault show --name mykv --query 'properties.vaultUri' -o tsv

### secrets
Store and retrieve secrets.

**Commands:**
- `az keyvault secret set --vault-name mykv --name db-password --value secret123`
- `az keyvault secret show --vault-name mykv --name db-password`
- `az keyvault secret list --vault-name mykv`
- `az keyvault secret delete --vault-name mykv --name db-password`
- `az keyvault secret set --vault-name mykv --name api-key --value $(openssl rand -hex 32)`

**Examples:**
- az keyvault secret set --vault-name mykv --name db-password --value 'p@ssw0rd!' --expires 2027-01-01T00:00:00Z
- az keyvault secret show --vault-name mykv --name db-password --query 'value' -o tsv
- az keyvault secret list --vault-name mykv --query '[].name' -o tsv

### keys-access
Manage keys and access policies.

**Commands:**
- `az keyvault key create --vault-name mykv --name rsa-key --protection software`
- `az keyvault key list --vault-name mykv`
- `az keyvault set-policy --vault-name mykv --object-id a1b2c3d4-e5f6-7890-abcd-ef1234567890 --secret-permissions get list set delete`
- `az keyvault show-policy --vault-name mykv --object-id a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- `az keyvault key show --vault-name mykv --name rsa-key`

**Examples:**
- az keyvault key create --vault-name mykv --name rsa-key --protection software --size 4096
- az keyvault set-policy --vault-name mykv --object-id a1b2c3d4-e5f6-7890-abcd-ef1234567890 --key-permissions get unwrapKey wrapKey
- az keyvault key list --vault-name mykv --query '[].{name:name,kid:key.kid}' -o table
