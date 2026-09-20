# api-sdk-engineer

Generates API SDKs with openapi-generator-cli: language selection, config files, additional properties, and batch generation for multi-language SDK publishing.

## Instructions

# API SDK Engineer

SDK generation from OpenAPI.

## What This Skill Does
- Generates idiomatic SDKs per language
- Customizes output with templates
- Publishes multi-language SDK artifacts

## When to Use
- Shipping official SDKs
- Keeping clients in sync with the API
- Multi-language support

## Real Commands

```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o sdk-ts
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o sdk-py
npx @openapitools/openapi-generator-cli batch openapi-generator-config.yaml
```

## Batch Config

```yaml
inputSpec: openapi.yaml
outputDir: sdks/
generators:
  typescript-axios:
    output: sdk-ts
  python:
    output: sdk-py
```

## Testing
- Compile generated SDKs
- Run smoke tests against a mock server
- Compare output across generator versions

## Best Practices
- Pin generator versions
- Commit generated SDKs per release
- Validate specs before generation

## Capabilities

### sdk-generation
Generate SDKs from OpenAPI specs

**Commands:**
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o sdk-ts`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o sdk-py`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o sdk-go`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o sdk-java --additional-properties=library=okhttp-gson`
- `npx @openapitools/openapi-generator-cli batch openapi-generator-config.yaml`

**Examples:**
- -g typescript-axios generates a TS axios SDK
- --additional-properties tunes generated code
- batch generates multiple languages at once

### template-customization
Customize generated SDK templates

**Commands:**
- `npx @openapitools/openapi-generator-cli config-help -g typescript-axios`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -t ./custom-templates -o sdk-ts`
- `npx @openapitools/openapi-generator-cli validate -i openapi.yaml`

**Examples:**
- -cli --help
- -api --help
