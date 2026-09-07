Creates, serves, invokes, and deploys Netlify Functions using the Netlify CLI. Supports local development with netlify dev, function testing with payloads, and production deployments.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `netlify functions:create`
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