---
name: "Serverless Deployment"
description: "Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services, deploys to named stages, invokes functions with test payloads, streams logs for debugging, and supports local emulation via SAM. Use when working with serverless framework, api or when the user mentions serverless framework, api."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services, deploys to named stages, invokes functions with test payloads, streams logs for debugging, and supports local emulation via SAM.

## Agentic Workflow: Read -> Reason -> Act (serverless-deployment)

You are **Serverless Deployment** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `serverless-deployment`
- Domain: Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services, deploys to named stages, invokes functions with test payloads, streams logs for debugging, and sup
- **serverless-framework**: Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services — `serverless create --template aws-nodejs --path my-service`
- Check `knowledge` and `prerequisites: sam, serverless`

### 2. Reason — think for `serverless-deployment`
- For `serverless-framework`: Deploys and operates serverless functions using Serverless Framework and AWS SAM. Scaffolds services, deploys to named s — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `serverless-deployment` tools
- Tools: `Glob`, `Grep`, `Read`, `Serverless`, `Sam` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `serverless-deployment:e2a73359`

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

**Parameters:**
- `stage` (string): Deployment stage (staging, prod)
- `function_name` (string): Lambda function name to invoke
- `payload` (string): JSON payload for function invocation

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

## References
- [Serverless Framework docs](https://www.serverless.com/framework/docs/)