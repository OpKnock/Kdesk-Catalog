---
applyTo: "**/*.json **/*.r **/*.sh"
---

# Aws Apigateway

Manages AWS API Gateway REST APIs: creating APIs and resources, deploying to stages, and invoking endpoints via curl.

## Instructions

# AWS API Gateway

## What this skill does

Manages AWS API Gateway REST APIs: creating APIs and resources, adding methods, deploying to stages, and invoking endpoints via curl and test-invoke-method.

## When to use

- Exposing Lambda functions or HTTP backends as managed APIs
- Adding a deployment/stage for a release
- Debugging a 502/500 from an integration

## Real commands

```bash
# Create an API
aws apigateway create-rest-api --name my-api

# List resources to find the root id
aws apigateway get-resources --rest-api-id abc123xyz

# Deploy to a stage
aws apigateway create-deployment --rest-api-id abc123xyz --stage-name prod

# Invoke from the CLI
aws apigateway test-invoke-method --rest-api-id abc123xyz --resource-id res123 --http-method GET --path-with-query-string '/users'

# Invoke from curl
curl -X POST https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/users -H "Content-Type: application/json" -d '{"name":"alice"}'
```

## Testing

- Use test-invoke-method to debug before deploying
- Check stage variables and logs after deployment

## Best practices

- Deploy to dev/stage/prod stages; never reuse a stage for releases
- Enable access logging and tracing for production stages
- Use usage plans + API keys for client throttling
- Prefer REST API vs HTTP API by feature needs (WAF, custom domains)

## Capabilities

### api-lifecycle
Create REST APIs, resources, methods, and deployments.

**Commands:**
- `aws apigateway create-rest-api --name my-api`
- `aws apigateway get-rest-apis`
- `aws apigateway get-resources --rest-api-id abc123xyz`
- `aws apigateway create-deployment --rest-api-id abc123xyz --stage-name prod`
- `aws apigateway get-stages --rest-api-id abc123xyz`

**Examples:**
- aws apigateway create-rest-api --name my-api --endpoint-configuration types=REGIONAL
- aws apigateway create-deployment --rest-api-id abc123xyz --stage-name prod --stage-description "v1.2.0"
- aws apigateway get-rest-apis --query 'items[].{id:id,name:name}' --output table

### invoke-and-test
Invoke deployed endpoints and test integration.

**Commands:**
- `curl -X POST https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/users -H "Content-Type: application/json" -d '{"name":"alice"}'`
- `curl -s https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/users?limit=10`
- `aws apigateway test-invoke-method --rest-api-id abc123xyz --resource-id res123 --http-method GET --path-with-query-string '/users'`
- `curl -s -o /dev/null -w "%{http_code}\n" https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/health`

**Examples:**
- curl -X POST https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/users -H "Content-Type: application/json" -d '{"name":"alice"}'
- aws apigateway test-invoke-method --rest-api-id abc123xyz --resource-id res123 --http-method GET --path-with-query-string '/users?limit=5'
- curl -i https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/users | head -30
