---
name: "azure-key-vault"
description: "Centralizes credentials and cryptographic material in a managed HSM-backed store using the Azure CLI: provisions vault instances, performs secret CRUD with versioning and expiry, manages asymmetric keys, and configures access policies or RBAC for service identities. Use when working with vault lifecycle, secrets, keys access, api or when the user mentions vault lifecycle, secrets, keys access, api."
license: "MIT"
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(az:*)"
---

Centralizes credentials and cryptographic material in a managed HSM-backed store using the Azure CLI: provisions vault instances, performs secret CRUD with versioning and expiry, manages asymmetric keys, and configures access policies or RBAC for service identities.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `az keyvault create --name mykv --resource-group rg`, `az keyvault secret set --vault-name mykv --name db-password `
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

**Parameters:**
- `vault_name` (string): Key Vault name
- `resource_group` (string): Resource group
- `location` (string): Azure region

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

**Parameters:**
- `secret_name` (string): Secret name
- `value` (string): Secret value
- `expires` (string): Expiry date ISO format

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

**Parameters:**
- `key_name` (string): Key name
- `protection` (string): software or hsm
- `permissions` (string): Permission set (get, list, set, delete, wrapKey...)

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

## References
- [Key Vault Docs](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Azure CLI keyvault Reference](https://learn.microsoft.com/en-us/cli/azure/keyvault)
