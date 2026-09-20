---
type: agent_requested
description: "Validates API contracts across OpenAPI, GraphQL, and Protobuf formats. Runs schema validation, backward-compatibility checks, and consumer-driven contract verification with Pact, integrating gates into CI/CD pipelines."
---

# API Contract Validator

Validates API contracts across OpenAPI, GraphQL, and Protobuf formats. Runs schema validation, backward-compatibility checks, and consumer-driven contract verification with Pact, integrating gates into CI/CD pipelines.

## Instructions

# API Contract Validator

## What this agent does

Ensures API contract quality across the lifecycle: schema validation for OpenAPI, GraphQL, and Protobuf;
automated breaking-change detection between versions; and consumer-driven contract testing with Pact.
Integrates validation gates into CI/CD to prevent incompatible changes from reaching production.

## When to use

- Validating API specifications before merge or release
- Detecting breaking changes in PRs or release branches
- Setting up consumer-driven contract pipelines with Pact Broker
- Enforcing API governance rules via Spectral rulesets
- Verifying provider compliance with consumer contracts

## Real commands

```bash
# Validate OpenAPI spec
swagger-cli validate ./api/openapi.yaml
spectral lint ./api/openapi.yaml --ruleset=spectral:oas

# Detect breaking changes
openapi-diff ./api/v1.yaml ./api/v2.yaml --format=markdown
graphql-inspector diff ./schema-v1.graphql ./schema-v2.graphql
buf breaking ./proto --against-input=.git#branch=main

# Pact workflow
pact-broker publish ./pacts --consumer-app-version=1.2.3 --branch=main
pact-provider-verifier --provider-base-url=http://localhost:8080 --pact-url=http://broker/pacts/provider/Consumer/latest
pact-broker can-i-deploy --pacticipant=OrdersAPI --version=1.2.3 --to=production
```

## Spectral ruleset example

```yaml
extends: ["spectral:oas"]
rules:
  operation-summary: error
  operation-description: warn
  no-server-example.com: error
```

## Pact consumer test (JavaScript)

```javascript
const { PactV3 } = require('@pact-foundation/pact');
const pact = new PactV3({ consumer: 'WebApp', provider: 'OrdersAPI' });

await pact.addInteraction()
  .uponReceiving('a request for orders')
  .withRequest({ method: 'GET', path: '/orders' })
  .willRespondWith({ status: 200, body: eachLike({ id: '1', total: 100 }) });
```

## Testing

- Run `swagger-cli validate` and `spectral lint` in CI on every spec change
- Run `openapi-diff` or `graphql-inspector diff` in PR checks
- Run `pact-provider-verifier` against provider in CI before deployment
- Use `pact-broker can-i-deploy` as a deployment gate

## Best practices

- Store specs in version control alongside code
- Use a shared Spectral ruleset across teams for consistent governance
- Publish pacts on every consumer build; verify on every provider build
- Configure `can-i-deploy` with environment-specific criteria
- Version Protobuf schemas with buf and enforce breaking-change policy

## Capabilities

### schema-validation
Validates OpenAPI, GraphQL SDL, and Protobuf schemas for structural correctness and spec compliance.

**Commands:**
- `swagger-cli validate openapi.yaml`
- `spectral lint openapi.yaml --ruleset=spectral:oas`
- `graphql-schema-linter schema.graphql`
- `buf lint protobuf/`

**Examples:**
- swagger-cli validate ./api/openapi.yaml
- spectral lint ./api/openapi.yaml --ruleset=spectral:oas --format=stylish
- graphql-schema-linter ./schema.graphql
- buf lint ./proto

### compatibility-check
Detects breaking changes between API specification versions using spectral, openapi-diff, and graphql-inspector.

**Commands:**
- `openapi-diff openapi-v1.yaml openapi-v2.yaml`
- `spectral lint openapi-v2.yaml --ruleset=./breaking-ruleset.yaml`
- `graphql-inspector diff schema-v1.graphql schema-v2.graphql`
- `buf breaking protobuf/v1 --against=protobuf/v2`

**Examples:**
- openapi-diff ./api/v1.yaml ./api/v2.yaml --format=markdown
- graphql-inspector diff ./schema-v1.graphql ./schema-v2.graphql --format=markdown
- buf breaking ./proto --against-input=.git#branch=main

### consumer-driven-contracts
Runs Pact consumer tests, publishes contracts to a broker, and verifies providers against published pacts.

**Commands:**
- `pact-broker publish pacts/ --consumer-app-version=1.2.3 --branch=main`
- `pact-provider-verifier --provider-base-url=http://localhost:8080 --pact-url=http://broker/pacts/provider/Consumer/latest`
- `pact-broker can-i-deploy --pacticipant=MyService --version=1.2.3 --to=production`

**Examples:**
- pact-broker publish ./pacts --consumer-app-version=1.2.3 --branch=main
- pact-provider-verifier --provider-base-url=http://localhost:8080 --pact-url=http://broker/pacts/provider/Consumer/latest
- pact-broker can-i-deploy --pacticipant=OrdersAPI --version=1.2.3 --to=production