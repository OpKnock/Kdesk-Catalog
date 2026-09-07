---
name: "azure"
description: "Operates Microsoft Azure with the az CLI: resource groups, VMs, AKS, functions, storage, and Azure AD. Use when working with azure core, azure aks, azure functions, cloud or when the user mentions azure core, azure aks, azure functions, cloud."
license: "MIT"
compatibility: "Requires func, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "cloud"}
allowed-tools: "Glob Grep Read Bash(az:*) Bash(func:*) Bash(kubectl:*)"
---

Operates Microsoft Azure with the az CLI: resource groups, VMs, AKS, functions, storage, and Azure AD.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `az login`, `az aks create --resource-group myrg --name mycluster --node-`
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
