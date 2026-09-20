# Env Config

Environment configuration management: load .env files, validate required variables, and inject config per environment without leaking secrets.

## Instructions

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