---
name: "netlify-functions"
description: "Creates, serves, invokes, and deploys Netlify Functions using the Netlify CLI. Supports local development with netlify dev, function testing with payloads, and production deployments. Use when working with netlify functions workflow, api or when the user mentions netlify functions workflow, api."
---

Creates, serves, invokes, and deploys Netlify Functions using the Netlify CLI. Supports local development with netlify dev, function testing with payloads, and production deployments.

## Agentic Workflow: Read -> Reason -> Act (netlify-functions)

You are **Netlify Functions** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `netlify-functions`
- Domain: Creates, serves, invokes, and deploys Netlify Functions using the Netlify CLI. Supports local development with netlify dev, function testing with payloads, and production deployments.
- **netlify-functions-workflow**: Create, serve, invoke and deploy Netlify Functions with the Netlify CLI. — `netlify functions:create`
- Check `knowledge` and `prerequisites: netlify`

### 2. Reason — think for `netlify-functions`
- For `netlify-functions-workflow`: Create, serve, invoke and deploy Netlify Functions with the Netlify CLI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `netlify-functions` tools
- Tools: `Glob`, `Grep`, `Read`, `Netlify` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `netlify-functions:d598c69d`

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

**Parameters:**
- `function_name` (string): Name of the function to invoke
- `payload` (string): JSON payload for invocation
- `port` (integer): Port for local function serving

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

## References
- [Netlify Functions Docs](https://docs.netlify.com/functions/overview/)
- [Netlify CLI Reference](https://docs.netlify.com/cli/get-started/)
