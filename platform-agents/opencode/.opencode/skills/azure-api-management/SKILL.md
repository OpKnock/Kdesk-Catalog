---
name: "azure-api-management"
description: "Operates Azure API Management gateways end-to-end: provisioning service tiers, importing OpenAPI definitions, applying policies (rate limit, CORS, transformation), managing subscription keys, and validating gateway routing with live curl calls. Use when working with apim service, api import, subscriptions or when the user mentions apim service, api import, subscriptions."
---

Operates Azure API Management gateways end-to-end: provisioning service tiers, importing OpenAPI definitions, applying policies (rate limit, CORS, transformation), managing subscription keys, and validating gateway routing with live curl calls.

## Agentic Workflow: Read -> Reason -> Act (azure-api-management)

You are **Azure Api Management** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `azure-api-management`
- Domain: Operates Azure API Management gateways end-to-end: provisioning service tiers, importing OpenAPI definitions, applying policies (rate limit, CORS, transformation), managing subscription keys, and vali
- **apim-service**: Create and manage API Management instances. — `az apim create --name my-apim --resource-group api-rg --publisher-email admin@co`
- **api-import**: Import and manage APIs in APIM. — `az apim api import --service-name my-apim -g api-rg --api-id petstore --path pet`
- **subscriptions**: Manage subscriptions and keys. — `az apim subscription list --service-name my-apim -g api-rg`
- Check `knowledge` references before acting

### 2. Reason — think for `azure-api-management`
- For `apim-service`: Create and manage API Management instances. — decide which checks to run
- For `api-import`: Import and manage APIs in APIM. — decide which checks to run
- For `subscriptions`: Manage subscriptions and keys. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `azure-api-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Az`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `azure-api-management:8df12e4b`

# Azure API Management

## What this skill does

Operates Azure API Management gateways end-to-end: provisioning service tiers, importing OpenAPI definitions, applying policies (rate limit, CORS, transformation), managing subscription keys, and validating gateway routing with live curl calls.

## When to use

- Exposing a backend API with rate limits, caching, or transformation
- Importing an OpenAPI spec to generate the gateway surface
- Issuing and rotating subscription keys

## Real commands

```bash
# Create a service
az apim create --name my-apim --resource-group api-rg --publisher-email admin@contoso.com --publisher-name Contoso --sku-name Consumption

# Import an OpenAPI spec
az apim api import --service-name my-apim -g api-rg --api-id petstore --path petstore --specification-format OpenApiJson --specification-path ./openapi.json

# List operations
az apim api operation list --service-name my-apim -g api-rg --api-id petstore --query '[].{method:method,url:urlTemplate}' -o table

# Subscription
az apim subscription create --service-name my-apim -g api-rg --name svc-key --owner-id svc-account --scope /apis

# Call through the gateway
curl -s -H "Ocp-Apim-Subscription-Key: $KEY" https://my-apim.azure-api.net/petstore/pets
```

## Testing

- Import then immediately list operations to verify the spec parsed
- Call the gateway URL with and without a key (401 without)

## Best practices

- Use Consumption/Developer tier for dev; Premium for production SLAs
- Set policies (rate limit, CORS) per API or product
- Rotate keys via regenerate-primary-key on a schedule

## Capabilities

### apim-service
Create and manage API Management instances.

**Parameters:**
- `sku` (string): Consumption, Developer, Basic, Standard, Premium
- `publisher_email` (string): Publisher email

**Commands:**
- `az apim create --name my-apim --resource-group api-rg --publisher-email admin@contoso.com --publisher-name Contoso --sku-name Consumption`
- `az apim show --name my-apim -g api-rg`
- `az apim list --resource-group api-rg`
- `az apim delete --name my-apim -g api-rg --yes`
- `az apim list-skus`

**Examples:**
- az apim create --name my-apim --resource-group api-rg --publisher-email admin@contoso.com --publisher-name Contoso --sku-name Developer
- az apim show --name my-apim -g api-rg --query 'gatewayUrl' -o tsv
- az apim list --resource-group api-rg --query '[].{name:name,sku:sku.name}' -o table

### api-import
Import and manage APIs in APIM.

**Parameters:**
- `api_id` (string): API identifier
- `path` (string): URL path suffix
- `spec_file` (string): OpenAPI spec file or URL

**Commands:**
- `az apim api import --service-name my-apim -g api-rg --api-id petstore --path petstore --specification-format OpenApiJson --specification-path ./openapi.json`
- `az apim api list --service-name my-apim -g api-rg`
- `az apim api show --service-name my-apim -g api-rg --api-id petstore`
- `az apim api operation list --service-name my-apim -g api-rg --api-id petstore`
- `az apim api update --service-name my-apim -g api-rg --api-id petstore --display-name "Pet Store v2"`

**Examples:**
- az apim api import --service-name my-apim -g api-rg --api-id petstore --path petstore --specification-format OpenApiJson --specification-url https://httpbin.org/openapi.json
- az apim api operation list --service-name my-apim -g api-rg --api-id petstore --query '[].{method:method,url:urlTemplate}' -o table
- az apim api list --service-name my-apim -g api-rg --query '[].{id:name,path:path}' -o table

### subscriptions
Manage subscriptions and keys.

**Parameters:**
- `subscription_name` (string): Subscription name
- `scope` (string): Scope: /apis, /apis/{api}, /products
- `owner_id` (string): Owner user/group id

**Commands:**
- `az apim subscription list --service-name my-apim -g api-rg`
- `az apim subscription create --service-name my-apim -g api-rg --name svc-key --owner-id svc-account --scope /apis`
- `az apim subscription show --service-name my-apim -g api-rg --subscription-id sub-12345`
- `az apim subscription regenerate-primary-key --service-name my-apim -g api-rg --subscription-id sub-12345`
- `curl -s -H "Ocp-Apim-Subscription-Key: $SUBSCRIPTION_KEY" https://my-apim.azure-api.net/petstore/pets`

**Examples:**
- az apim subscription create --service-name my-apim -g api-rg --name svc-key --owner-id svc-account --scope /apis --primary-key $(openssl rand -hex 16)
- az apim subscription regenerate-secondary-key --service-name my-apim -g api-rg --subscription-id sub-12345
- curl -s -H "Ocp-Apim-Subscription-Key: $KEY" https://my-apim.azure-api.net/petstore/pets?limit=5

## References
- [API Management Docs](https://learn.microsoft.com/en-us/azure/api-management/)
- [Azure CLI apim Reference](https://learn.microsoft.com/en-us/cli/azure/apim)
