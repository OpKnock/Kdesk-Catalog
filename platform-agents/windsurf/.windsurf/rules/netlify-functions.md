---
trigger: glob
description: "Creates, serves, invokes, and deploys Netlify Functions using the Netlify CLI. Supports local development with netlify dev, function testing with payloads, and production deployments."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Netlify Functions

Creates, serves, invokes, and deploys Netlify Functions using the Netlify CLI. Supports local development with netlify dev, function testing with payloads, and production deployments.

## Instructions

# Netlify Functions

Netlify Functions run serverless backend code alongside static sites on Netlify.

## What this skill does

- Scaffolds new functions from templates
- Serves and invokes functions locally
- Deploys to production with the CLI

## When to use

- Serverless APIs for Jamstack sites
- Form handlers and webhooks

## Real commands

```bash
# Authenticate and init
netlify login
netlify init

# Create a function
netlify functions:create

# Local serving
netlify functions:serve --port 8888
netlify dev

# Invoke with payload
netlify functions:invoke my-function --payload '{"name":"alice"}'

# Deploy
netlify deploy --prod
netlify deploy --prod --build
```

## Handler example

```js
exports.handler = async (event, context) => ({
  statusCode: 200,
  body: JSON.stringify({ hello: event.queryStringParameters.name }),
});
```

## Best practices

- Test locally before deploying
- Keep functions pure: no shared mutable state
- Use environment variables for secrets via netlify env

## Capabilities

### netlify-functions-workflow
Create, serve, invoke and deploy Netlify Functions with the Netlify CLI.

**Commands:**
- `netlify functions:create`
- `netlify functions:serve --port 8888`
- `netlify functions:invoke my-function`
- `netlify dev`
- `netlify deploy --prod`

**Examples:**
- netlify functions:invoke my-function --payload '{"name":"alice"}'
- netlify functions:serve --functions build/functions
- netlify deploy --prod --build
