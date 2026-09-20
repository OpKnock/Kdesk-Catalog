---
applyTo: "**/*.json **/*.r **/*.sh"
---

Operates Azure API Management gateways end-to-end: provisioning service tiers, importing OpenAPI definitions, applying policies (rate limit, CORS, transformation), managing subscription keys, and validating gateway routing with live curl calls.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `az apim create --name my-apim --resource-group api-rg --publ`, `az apim api import --service-name my-apim -g api-rg --api-id`
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
