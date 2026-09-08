---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Implements OAuth2 social sign-in with GitHub and Google. Completes authorization code exchanges, fetches profile data from userinfo endpoints, maps provider identities to local accounts by stable provider ID, and verifies state parameters to prevent CSRF.

## Agentic Workflow: Read -> Reason -> Act (social-login)

You are **Social Login** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `social-login`
- Domain: Implements OAuth2 social sign-in with GitHub and Google. Completes authorization code exchanges, fetches profile data from userinfo endpoints, maps provider identities to local accounts by stable prov
- **oauth-social-login**: Implements OAuth2 social sign-in with GitHub and Google. Completes authorization code exchanges, fet — `curl -X POST https://github.com/login/oauth/access_token -H "Accept: application`
- Check `knowledge` references before acting

### 2. Reason — think for `social-login`
- For `oauth-social-login`: Implements OAuth2 social sign-in with GitHub and Google. Completes authorization code exchanges, fetches profile data fr — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `social-login` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `social-login:a8eca7f3`

# Social Login

Hand-crafted skill for OAuth2 social sign-in with GitHub and Google.

## What this skill does

- Completes the authorization code exchange for GitHub and Google
- Fetches profile data from userinfo endpoints
- Maps provider identity to local accounts

## When to use

- Adding Sign in with GitHub/Google to an app
- Debugging token exchange failures in CI
- Verifying the claims your app receives

## Real commands

```bash
# GitHub: exchange the code (from /login/oauth/authorize redirect)
curl -X POST https://github.com/login/oauth/access_token -H "Accept: application/json" -d "client_id=$GITHUB_CLIENT_ID&client_secret=$GITHUB_CLIENT_SECRET&code=$CODE" | jq -r .access_token

# GitHub profile
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" https://api.github.com/user | jq '{login, id, email}'

# Google: exchange the code
curl -X POST https://oauth2.googleapis.com/token -d "client_id=$GOOGLE_CLIENT_ID&client_secret=$GOOGLE_CLIENT_SECRET&code=$CODE&redirect_uri=http://localhost:3000/callback&grant_type=authorization_code" | jq -r .access_token

# Google userinfo
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" https://www.googleapis.com/oauth2/v3/userinfo | jq '.sub, .email'
```

## Flow

1. Redirect user to the provider's authorize URL
2. Provider redirects back with ?code=
3. Exchange the code for tokens (commands above)
4. Fetch profile, upsert local user by provider id

## Testing

```bash
# Local callback test
curl -X POST https://github.com/login/oauth/access_token -H "Accept: application/json" -d "client_id=$GITHUB_CLIENT_ID&client_secret=$GITHUB_CLIENT_SECRET&code=test" | jq
```

## Best practices

- Match users by provider id, not email (emails change)
- Store only the tokens you need; prefer short-lived access tokens
- Verify the state parameter on the callback to block CSRF

## Capabilities

### oauth-social-login
Implements OAuth2 social sign-in with GitHub and Google. Completes authorization code exchanges, fetches profile data from userinfo endpoints, maps provider identities to local accounts by stable provider ID, and verifies state parameters to prevent CSRF.

**Parameters:**
- `github_client_id` (string): GitHub OAuth application client ID
- `github_client_secret` (string): GitHub OAuth application client secret
- `google_client_id` (string): Google OAuth client ID
- `google_client_secret` (string): Google OAuth client secret
- `redirect_uri` (string): Registered redirect URI for OAuth callback

**Commands:**
- `curl -X POST https://github.com/login/oauth/access_token -H "Accept: application/json" -d "client_id=$GITHUB_CLIENT_ID&client_secret=$GITHUB_CLIENT_SECRET&code=$AUTH_CODE"`
- `curl -H "Authorization: Bearer $ACCESS_TOKEN" https://api.github.com/user`
- `curl -X POST https://oauth2.googleapis.com/token -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=$GOOGLE_CLIENT_ID&client_secret=$GOOGLE_CLIENT_SECRET&code=$AUTH_CODE&grant_type=authorization_code&redirect_uri=$REDIRECT_URI"`
- `curl -H "Authorization: Bearer $ACCESS_TOKEN" https://www.googleapis.com/oauth2/v2/userinfo`

**Examples:**
- curl -X POST https://github.com/login/oauth/access_token -H "Accept: application/json" -d "client_id=$GITHUB_CLIENT_ID&client_secret=$GITHUB_CLIENT_SECRET&code=$AUTH_CODE"
- curl -H "Authorization: Bearer $ACCESS_TOKEN" https://api.github.com/user
- curl -X POST https://oauth2.googleapis.com/token -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=$GOOGLE_CLIENT_ID&client_secret=$GOOGLE_CLIENT_SECRET&code=$AUTH_CODE&grant_type=authorization_code&redirect_uri=$REDIRECT_URI"
- curl -H "Authorization: Bearer $ACCESS_TOKEN" https://www.googleapis.com/oauth2/v2/userinfo

## References
- [GitHub OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)
