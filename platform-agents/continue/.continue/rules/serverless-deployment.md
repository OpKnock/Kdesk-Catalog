---
name: "Serverless Deployment"
description: "Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services, deploys to named stages, invokes functions with test payloads, streams logs for debugging, and supports local emulation via SAM."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Serverless Deployment

Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services, deploys to named stages, invokes functions with test payloads, streams logs for debugging, and supports local emulation via SAM.

## Instructions

# Serverless Deployment

Hand-crafted skill for deploying serverless functions safely.

## What this skill does

- Scaffolds services with the Serverless Framework and SAM templates
- Deploys to named stages and invokes functions for verification
- Streams function logs for debugging

## When to use

- Shipping a function-based service to production
- Reproducing an invocation locally before deploy
- Promoting from staging to prod with one command

## Real commands

```bash
# Scaffold
serverless create --template aws-nodejs --path my-service
cd my-service && npm install

# Deploy per stage
serverless deploy --stage staging
serverless deploy --stage prod

# Invoke with a payload
serverless invoke -f hello --stage prod --data '{"name":"Ada"}'

# Tail logs
serverless logs -f hello -t

# AWS SAM equivalents
sam build
sam local invoke HelloWorldFunction --event event.json
sam deploy --guided
```

## serverless.yml

```yaml
service: my-service
provider:
  name: aws
  runtime: nodejs20.x
  region: eu-west-1
functions:
  hello:
    handler: handler.hello
    events:
      - httpApi:
          path: /hello
          method: get
```

## Testing

```bash
serverless deploy --stage staging
serverless invoke -f hello --stage staging --data '{"name":"test"}'
serverless logs -f hello --stage staging
```

## Best practices

- Deploy to staging, smoke-test, then promote to prod
- Pin the runtime and region in serverless.yml
- Keep functions small; delegate heavy work to queues

## Capabilities

### serverless-framework
Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services, deploys to named stages, invokes functions with test payloads, streams logs for debugging, and supports local emulation via SAM.

**Commands:**
- `serverless create --template aws-nodejs --path my-service`
- `serverless deploy --stage staging`
- `serverless deploy --stage prod`
- `serverless invoke -f hello --stage prod --data '{"name":"Ada"}'`
- `serverless logs -f hello -t`
- `sam build`
- `sam local invoke HelloWorldFunction --event event.json`
- `sam deploy --guided`

**Examples:**
- serverless create --template aws-nodejs --path my-service
- serverless deploy --stage prod
- serverless invoke -f hello --stage prod --data '{"name":"Ada"}'
- sam build
- sam local invoke HelloWorldFunction --event event.json
- sam deploy --guided