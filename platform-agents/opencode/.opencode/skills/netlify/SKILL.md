---
name: "netlify"
description: "Deploys frontend apps with Netlify: CLI deploys, build configuration, environment variables, and edge functions. Use when working with netlify cli, netlify config, cloud or when the user mentions netlify cli, netlify config, cloud."
---

Deploys frontend apps with Netlify: CLI deploys, build configuration, environment variables, and edge functions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g netlify-cli`, `netlify env:set API_KEY abc123`
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

# Netlify

Deploy frontend apps with the Netlify CLI.

## When to Use

- Static sites and SPAs with CDN delivery
- JAMstack deploys with preview deployments
- Serverless functions (Netlify Functions)
- Managed forms and identity without a backend

## Commands

```bash
# Setup
npm install -g netlify-cli
netlify init

# Deploy
netlify deploy --dir dist
netlify deploy --prod
netlify deploy --dir dist --prod

# Local dev
netlify dev

# Env vars
netlify env:set API_KEY abc123
netlify env:set --context production API_URL https://api.example.com
netlify env:list
netlify env:unset API_KEY

# Status and functions
netlify status
netlify functions:list
netlify functions:serve
```

## netlify.toml Example

```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[redirects]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Best Practices

- Use deploy previews for PR review environments
- Set context-specific env vars (production vs preview)
- Keep redirects and headers in netlify.toml for versioning
- Run netlify deploy --build in CI with a pinned CLI version
- Test functions locally with netlify functions:serve
- Use deploy contexts to gate production promotions

## Capabilities

### netlify-cli
Build, deploy, and manage Netlify sites.

**Parameters:**
- `dir` (string): Publish directory
- `prod` (boolean): Deploy to production

**Commands:**
- `npm install -g netlify-cli`
- `netlify init`
- `netlify deploy`
- `netlify deploy --prod`
- `netlify dev`

**Examples:**
- netlify deploy --dir dist --prod
- netlify deploy --build --prod
- netlify open

### netlify-config
Manage environment variables and site settings.

**Parameters:**
- `key` (string): Env var name
- `value` (string): Env var value

**Commands:**
- `netlify env:set API_KEY abc123`
- `netlify env:list`
- `netlify env:unset API_KEY`
- `netlify status`
- `netlify functions:list`

**Examples:**
- netlify env:set --context production API_URL https://api.example.com
- netlify functions:serve
- netlify status

## References
- [Netlify Docs](https://docs.netlify.com)
- [Netlify CLI](https://cli.netlify.com)
