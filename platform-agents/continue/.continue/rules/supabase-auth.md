---
name: "Supabase Auth"
description: "Drive Supabase Auth flows via REST and the Supabase CLI. Use when working with supabase auth flow, api or when the user mentions supabase auth flow, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Drive Supabase Auth flows via REST and the Supabase CLI.

## Agentic Workflow: Read -> Reason -> Act (supabase-auth)

You are **Supabase Auth** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `supabase-auth`
- Domain: Drive Supabase Auth flows via REST and the Supabase CLI.
- **supabase-auth-flow**: Drive Supabase Auth flows via REST and the Supabase CLI — `supabase init && supabase start`
- Check `knowledge` and `prerequisites: supabase`

### 2. Reason — think for `supabase-auth`
- For `supabase-auth-flow`: Drive Supabase Auth flows via REST and the Supabase CLI — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `supabase-auth` tools
- Tools: `Glob`, `Grep`, `Read`, `Supabase`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `supabase-auth:6bde29cd`

# Supabase Auth

Hand-crafted skill for authentication with Supabase Auth (GoTrue).

## What this skill does

- Boots a local Supabase stack with the CLI
- Calls signup, token, user, and logout endpoints directly
- Uses the anon key for public endpoints and access tokens for private ones

## When to use

- Adding email/password auth to an app on Supabase
- Debugging auth API behavior from the terminal
- Testing token refresh and logout flows

## Real commands

```bash
# Local stack
supabase init && supabase start

# Sign up
curl -X POST "https://your-project.supabase.co/auth/v1/signup" -H "apikey: $SUPABASE_ANON_KEY" -H "Content-Type: application/json" -d "{\"email\":\"ada@example.com\",\"password\":\"supersecret\"}"

# Sign in (password grant)
curl -X POST "https://your-project.supabase.co/auth/v1/token?grant_type=password" -H "apikey: $SUPABASE_ANON_KEY" -d "{\"email\":\"ada@example.com\",\"password\":\"supersecret\"}" | jq -r .access_token

# Refresh
curl -X POST "https://your-project.supabase.co/auth/v1/token?grant_type=refresh_token" -H "apikey: $SUPABASE_ANON_KEY" -d "refresh_token=$REFRESH" | jq -r .access_token

# Who am I?
curl -s "https://your-project.supabase.co/auth/v1/user" -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN" | jq ".email"

# Logout
curl -X POST "https://your-project.supabase.co/auth/v1/logout" -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN"
```

## Token types

- anon key: public operations (signup, signin)
- access_token: authenticated requests to auth and PostgREST
- refresh_token: exchanged at /auth/v1/token?grant_type=refresh_token

## Testing

```bash
supabase start

TOKEN=$(curl -X POST "http://localhost:54321/auth/v1/token?grant_type=password" -H "apikey: $SUPABASE_ANON_KEY" -d "{\"email\":\"ada@example.com\",\"password\":\"supersecret\"}" | jq -r .access_token)

echo $TOKEN
```

## Best practices

- Keep the anon key public-safe; the service_role key must stay server-side
- Enforce RLS policies per table so tokens do not grant table access
- Store refresh tokens server-side when doing magic-link or session flows

## Capabilities

### supabase-auth-flow
Drive Supabase Auth flows via REST and the Supabase CLI

**Parameters:**
- `anon_key` (string): Supabase anon (public) API key
- `grant_type` (string): password, refresh_token, or otp for /auth/v1/token
- `email` (string): User email for signup/signin

**Commands:**
- `supabase init && supabase start`
- `curl -X POST "https://your-project.supabase.co/auth/v1/signup" -H "apikey: $SUPABASE_ANON_KEY" -H "Content-Type: application/json" -d "{\"email\":\"ada@localhost\",\"password\":\"supersecret\"}"`
- `curl -X POST "https://your-project.supabase.co/auth/v1/token?grant_type=password" -H "apikey: $SUPABASE_ANON_KEY" -d "{\"email\":\"ada@localhost\",\"password\":\"supersecret\"}" | jq -r .access_token`
- `curl -X POST "https://your-project.supabase.co/auth/v1/logout" -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN"`
- `supabase functions deploy auth-helper`

**Examples:**
- curl -X POST "https://your-project.supabase.co/auth/v1/signup" -H "apikey: $SUPABASE_ANON_KEY" -d "{\"email\":\"ada@localhost\",\"password\":\"supersecret\"}"
- curl -X POST "https://your-project.supabase.co/auth/v1/token?grant_type=refresh_token" -H "apikey: $SUPABASE_ANON_KEY" -d "refresh_token=$REFRESH" | jq -r .access_token
- curl -s "https://your-project.supabase.co/auth/v1/user" -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN" | jq ".email"

## References
- [Supabase Auth docs](https://supabase.com/docs/guides/auth)
- [Supabase CLI reference](https://supabase.com/docs/reference/cli)