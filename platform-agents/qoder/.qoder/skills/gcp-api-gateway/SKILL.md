---
name: "gcp-api-gateway"
description: "Create API configs, deploy gateways, and manage keys via gcloud. API keys for access control.'. Use when working with gcp api gateway or when the user mentions gcp api gateway."
license: "MIT"
compatibility: "Requires gcloud."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(gcloud:*)"
---

Create API configs, deploy gateways, and manage keys via gcloud. API keys for access control.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gcloud api-gateway apis create orders-api`
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

# GCP API Gateway

## What this skill does

GCP API Gateway exposes backend services behind a managed gateway driven by OpenAPI specs. You create an API config from the spec, deploy a gateway, and secure it with API keys.

## When to use

- Publishing internal Cloud Run/Cloud Functions behind one front door
- Applying quota and API-key auth without code changes
- Versioning backends per config

## Real commands

```bash
# Create the API
 gcloud api-gateway apis create orders-api

# Create a config from the OpenAPI spec
gcloud api-gateway api-configs create orders-v1 --api=orders-api --openapi-spec=openapi.yaml --display-name=orders-v1

# Deploy the gateway
 gcloud api-gateway gateways create orders-gw --api=orders-api --api-config=orders-v1 --location=us-central1

# Get the hostname
 gcloud api-gateway gateways describe orders-gw --location=us-central1 --format='value(defaultHostname)'

# Create an API key
 gcloud services api-keys create --display-name=orders-key --api-target=service=orders-gw
```

## OpenAPI snippet for gateway

```yaml
openapi: 3.0.1
info:
  title: Orders API
  version: v1
securityDefinitions:
  api_key:
    type: apiKey
    name: key
    in: query
x-google-backend:
  address: https://orders-backend-abc-uc.a.run.app
```

## Testing

```bash
HOST=$(gcloud api-gateway gateways describe orders-gw --location=us-central1 --format='value(defaultHostname)')
curl -s "https://$HOST/v1/orders?key=$API_KEY" | jq
```

## Best practices

- Name configs by version (orders-v1, orders-v2) and deploy gateways per environment.
- Use the `x-google-backend` extension to wire Cloud Run/Functions.
- Protect the key: query param keys are visible in logs; prefer headers.
- Set quota per config in the OpenAPI `x-google-quota` extension.
- Pin the gateway location near your backend.

## Capabilities

### gcp-api-gateway
Create API configs, deploy gateways, and manage keys via gcloud.

**Parameters:**
- `api-name` (string): API Gateway API name
- `config-name` (string): API config version name
- `region` (string): Gateway location like us-central1

**Commands:**
- `gcloud api-gateway apis create orders-api`
- `gcloud api-gateway api-configs create orders-v1 --api=orders-api --openapi-spec=openapi.yaml --display-name=orders-v1`
- `gcloud api-gateway gateways create orders-gw --api=orders-api --api-config=orders-v1 --location=us-central1`
- `gcloud api-gateway gateways describe orders-gw --location=us-central1 --format='value(defaultHostname)'`
- `gcloud services api-keys create --display-name=orders-key --api-target=service=orders-gw`

**Examples:**
- gcloud api-gateway apis create orders-api && gcloud api-gateway api-configs create orders-v1 --api=orders-api --openapi-spec=openapi.yaml
- gcloud api-gateway gateways create orders-gw --api=orders-api --api-config=orders-v1 --location=us-central1
- gcloud api-gateway gateways describe orders-gw --location=us-central1 --format='value(defaultHostname)'

## References
- [API Gateway overview](https://cloud.google.com/api-gateway/docs)
- [API Gateway gcloud reference](https://cloud.google.com/sdk/gcloud/reference/api-gateway)
