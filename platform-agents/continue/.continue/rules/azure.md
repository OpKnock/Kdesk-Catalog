---
name: "azure"
description: "Operates Microsoft Azure with the az CLI: resource groups, VMs, AKS, functions, storage, and Azure AD. Use when working with azure core, azure aks, azure functions, cloud or when the user mentions azure core, azure aks, azure functions, cloud."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.tf"]
alwaysApply: false
---

Operates Microsoft Azure with the az CLI: resource groups, VMs, AKS, functions, storage, and Azure AD.

## Agentic Workflow: Read -> Reason -> Act (azure)

You are **azure** (cloud/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — cloud context for `azure`
- Domain: Operates Microsoft Azure with the az CLI: resource groups, VMs, AKS, functions, storage, and Azure AD.
- **azure-core**: Manage subscriptions, groups, and storage. — `az login`
- **azure-aks**: Manage AKS clusters and get credentials. — `az aks create --resource-group myrg --name mycluster --node-count 3 --enable-man`
- **azure-functions**: Deploy and manage Azure Functions. — `func azure functionapp publish myfuncapp`
- Check `knowledge` and `prerequisites: func, kubectl`

### 2. Reason — think for `azure`
- For `azure-core`: Manage subscriptions, groups, and storage. — decide which checks to run
- For `azure-aks`: Manage AKS clusters and get credentials. — decide which checks to run
- For `azure-functions`: Deploy and manage Azure Functions. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `azure` tools
- Tools: `Glob`, `Grep`, `Read`, `Az`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `azure:8d9b5055`

# Azure

Operate Azure with the az CLI.

## When to Use

- Managing resource groups, VMs, and storage
- AKS cluster provisioning and credential access
- Deploying Azure Functions
- Role-based access control (Azure AD/RBAC)

## Commands

```bash
# Auth and context
az login
az account list --output table
az account set --subscription "My Sub"

# Resource groups and storage
az group create --name myrg --location eastus
az storage account create --name mystore --resource-group myrg --sku Standard_LRS
az storage container list --account-name mystore

# AKS
az aks create --resource-group myrg --name mycluster --node-count 3 --enable-managed-identity
az aks get-credentials --resource-group myrg --name mycluster
az aks scale --resource-group myrg --name mycluster --node-count 5
kubectl get nodes

# Functions
func init --python
func azure functionapp publish myfuncapp
az functionapp config appsettings set --name myfuncapp --resource-group myrg --settings "KEY=VALUE"
```

## Best Practices

- Use managed identity over service principals where possible
- Scope RBAC roles to the resource group level
- Name resources with a consistent convention
- Use az aks get-credentials --admin only for break-glass
- Enable diagnostics and metrics for every service
- Prefer Bicep/Terraform for reproducible infrastructure

## Capabilities

### azure-core
Manage subscriptions, groups, and storage.

**Parameters:**
- `resource-group` (string): Resource group name
- `location` (string): Azure region

**Commands:**
- `az login`
- `az account list --output table`
- `az group create --name myrg --location eastus`
- `az storage account create --name mystore --resource-group myrg --sku Standard_LRS`
- `az account show --query "user.name"`

**Examples:**
- az group list --output table
- az storage container list --account-name mystore
- az account set --subscription "My Sub"

### azure-aks
Manage AKS clusters and get credentials.

**Parameters:**
- `cluster` (string): AKS cluster name
- `node-count` (integer): Number of worker nodes

**Commands:**
- `az aks create --resource-group myrg --name mycluster --node-count 3 --enable-managed-identity`
- `az aks get-credentials --resource-group myrg --name mycluster`
- `az aks list`
- `az aks scale --resource-group myrg --name mycluster --node-count 5`
- `kubectl get nodes`

**Examples:**
- az aks get-credentials --resource-group myrg --name mycluster --admin
- az aks show --resource-group myrg --name mycluster --query "powerState.code"

### azure-functions
Deploy and manage Azure Functions.

**Parameters:**
- `app` (string): Function app name
- `runtime` (string): Function runtime: python, node, dotnet

**Commands:**
- `func azure functionapp publish myfuncapp`
- `az functionapp list --resource-group myrg`
- `az functionapp config appsettings set --name myfuncapp --resource-group myrg --settings "KEY=VALUE"`
- `func init --python`

**Examples:**
- func azure functionapp publish myfuncapp --build remote
- az functionapp show --name myfuncapp --query "defaultHostName"

## References
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)
- [Azure for Developers](https://learn.microsoft.com/azure/)