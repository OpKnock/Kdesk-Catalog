---
trigger: glob
description: "Environment configuration management: load .env files, validate required variables, and inject config per environment without leaking secrets. Use when working with env management, api or when the user mentions env management, api."
globs: ["**/*.java", "**/*.py", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
---

Environment configuration management: load .env files, validate required variables, and inject config per environment without leaking secrets.

## Agentic Workflow: Read -> Reason -> Act (env-config)

You are **Env Config** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `env-config`
- Domain: Environment configuration management: load .env files, validate required variables, and inject config per environment without leaking secrets.
- **env-management**: Load, validate, and debug environment variables across dev/staging/prod. — `node -r dotenv/config index.js`
- Check `knowledge` and `prerequisites: env, grep, node, python`

### 2. Reason — think for `env-config`
- For `env-management`: Load, validate, and debug environment variables across dev/staging/prod. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `env-config` tools
- Tools: `Glob`, `Read`, `Bash`, `Grep`, `Env` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `env-config:f673a26e`

# Env Config

## What this skill does

Environment configuration keeps settings out of code: everything that varies between environments lives in env vars. This skill covers dotenv loading, validation, and safe debugging.

## When to use

- Setting up a new project's configuration layer
- Debugging why an app uses the wrong database
- Auditing that no secret sits in committed .env files

## Real commands

```bash
# Load .env in Node without code changes
node -r dotenv/config index.js

# Verify a loaded value (name only, never the value)
node -e "require('dotenv').config(); console.log(process.env.NODE_ENV)"

# List variable NAMES from .env (values redacted)
grep -E '^[A-Z_]+=' .env | sed 's/=.*/=<redacted>/'

# Compare what the shell actually has
env | grep -iE '^(DATABASE|API_KEY|PORT)=' | cut -d= -f1
```

## Validation example (Node)

```javascript
const required = ['DATABASE_URL', 'JWT_SECRET', 'PORT']
const missing = required.filter(k => !process.env[k])
if (missing.length) {
  throw new Error(`Missing required env vars: ${missing.join(', ')}`)
}
```

## Testing

```bash
# Start the app with a test env and confirm config is read
NODE_ENV=test PORT=4000 node -r dotenv/config index.js
curl -s localhost:4000/health | jq '.env'
```

## Best practices

- Commit `.env.example` with placeholder values; gitignore `.env`.
- Fail fast at startup when required vars are missing.
- Never log env values; log names and presences only.
- Prefer tooling like Doppler/aws ssm for prod; keep dotenv for local only.
- Parse booleans/numbers explicitly instead of string truthiness.

## Capabilities

### env-management
Load, validate, and debug environment variables across dev/staging/prod.

**Parameters:**
- `env-file` (string): Path to the .env file
- `var-name` (string): Variable to validate or print
- `required-vars` (array): List of variables that must be set for the app to start

**Commands:**
- `node -r dotenv/config index.js`
- `node -e "require('dotenv').config(); console.log(process.env.NODE_ENV)"`
- `grep -E '^[A-Z_]+=' .env | sed 's/=.*/=[REDACTED]/'`
- `env | grep -iE '^(DATABASE|API_KEY|PORT)=' | cut -d= -f1`
- `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DATABASE_URL', 'MISSING'))"`

**Examples:**
- node -r dotenv/config index.js
- grep -E '^[A-Z_]+=' .env | sed 's/=.*/=[REDACTED]/'
- env | grep -iE '^(DATABASE|API_KEY|PORT)=' | cut -d= -f1

## References
- [The Twelve-Factor App: Config](https://12factor.net/config)
