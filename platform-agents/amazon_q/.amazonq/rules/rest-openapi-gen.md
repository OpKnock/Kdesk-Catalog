# Rest Openapi Gen

Expert OpenAPI generation reference for validating specs, linting with Redocly, and generating typed clients and server stubs with openapi-generator across languages.

## Instructions

# OpenAPI Code Generation

Expert skill for generating clients and servers from OpenAPI specs.

## What this skill does

- Validates specs so generation does not fail halfway
- Lints for spec quality with Redocly rules
- Generates typed SDKs and server stubs in many languages

## When to use

- Contract-first development: spec drives all consumers
- Producing versioned client SDKs for each release
- Keeping server stubs in sync with the documented API

## Real commands

```bash
# Check the CLI
npx @openapitools/openapi-generator-cli version

# Validate the spec first
npx @openapitools/openapi-generator-cli validate -i openapi.yaml

# Python client
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o out/python

# TypeScript axios client with interfaces
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o out/ts --additional-properties=withInterfaces=true

# Go client
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o out/go

# Lint the spec before merging
npx @redocly/cli lint openapi.yaml
```

## Spec quality gates

```bash
# Redocly config to fail CI on errors
npx @redocly/cli lint openapi.yaml --config redocly.yaml
```

## Testing generated code

```bash
cd out/python && pip install -e .
python -c 'from openapi_client import Configuration, ApiClient, OrdersApi; print(OrdersApi(ApiClient(Configuration(host="http://localhost:8080"))))'
```

## Best practices

- Always validate before generate to get clean error messages
- Commit the spec, regenerate SDKs per release tag
- Pin the CLI version in package.json to keep output deterministic

## Capabilities

### openapi-generate
Validate, lint, and generate code from OpenAPI specifications

**Commands:**
- `npx @openapitools/openapi-generator-cli version`
- `npx @openapitools/openapi-generator-cli validate -i openapi.yaml`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o out/python`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o out/ts --additional-properties=withInterfaces=true`
- `npx @redocly/cli lint openapi.yaml`

**Examples:**
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o out/go
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o out/java --library=webclient
- npx @redocly/cli lint openapi.yaml --config redocly.yaml