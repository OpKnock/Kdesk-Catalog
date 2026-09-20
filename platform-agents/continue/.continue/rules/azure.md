---
name: "azure"
description: "Operates Microsoft Azure with the az CLI: resource groups, VMs, AKS, functions, storage, and Azure AD."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.tf"]
alwaysApply: false
---

# azure

Operates Microsoft Azure with the az CLI: resource groups, VMs, AKS, functions, storage, and Azure AD.

## Instructions

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

**Commands:**
- `func azure functionapp publish myfuncapp`
- `az functionapp list --resource-group myrg`
- `az functionapp config appsettings set --name myfuncapp --resource-group myrg --settings "KEY=VALUE"`
- `func init --python`

**Examples:**
- func azure functionapp publish myfuncapp --build remote
- az functionapp show --name myfuncapp --query "defaultHostName"