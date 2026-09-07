---
trigger: glob
description: "Federated identity and SSO: configure Keycloak clients and realms, exchange tokens via OIDC, and test IdP-driven login flows. Use when working with oidc sso, api or when the user mentions oidc sso, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

Federated identity and SSO: configure Keycloak clients and realms, exchange tokens via OIDC, and test IdP-driven login flows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s 'http://localhost:8080/realms/master/protocol/openid`
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

# Federated Identity

## What this skill does

Federated identity lets one identity provider (Keycloak, Entra ID, Google) authenticate users across many apps via OIDC/SAML. This skill covers Keycloak realm/client administration and token flows.

## When to use

- Implementing SSO across internal apps
- Federating users from Google/GitHub as an IdP
- Verifying token issuance and key rotation

## Real commands

```bash
# Get an admin token
curl -s 'http://localhost:8080/realms/master/protocol/openid-connect/token' -d 'grant_type=client_credentials&client_id=admin-cli&client_secret=secret' | jq -r '.access_token'

# Create a realm
curl -s -X POST 'http://localhost:8080/admin/realms' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{"realm":"acme","enabled":true}' | jq

# Discover OIDC endpoints
curl -s 'http://localhost:8080/realms/acme/.well-known/openid-configuration' | jq '.authorization_endpoint, .token_endpoint, .jwks_uri'

# Password grant (test users)
curl -s 'http://localhost:8080/realms/acme/protocol/openid-connect/token' -d 'grant_type=password&client_id=web&username=alice&password=secret' | jq -r '.access_token'

# JWKS for verifying tokens
curl -s 'http://localhost:8080/realms/acme/protocol/openid-connect/certs' | jq '.keys[0].kid'
```

## Best practices

- Validate tokens via JWKS keys and `iss`/`aud` claims, never blindly.
- Use the authorization_code flow for browsers; never password grant in production.
- Configure realm keys with rotation; monitor the `kid` change.
- Map IdP claims to realm roles at the IdP federation level.
- Test realm backup/export (`/admin/realms/acme/partial-export`) before big changes.

## Testing

```bash
# End-to-end: discover -> auth -> introspect
TOKEN=$(curl -s 'http://localhost:8080/realms/acme/protocol/openid-connect/token' -d 'grant_type=password&client_id=web&username=alice&password=secret' | jq -r '.access_token')
curl -s 'http://localhost:8080/realms/acme/protocol/openid-connect/userinfo' -H "Authorization: Bearer $TOKEN" | jq
```

## Capabilities

### oidc-sso
Manage Keycloak realms/clients, get tokens via the OIDC flow, and verify user federation.

**Parameters:**
- `realm` (string): Keycloak realm name
- `client-id` (string): OIDC client registered in the realm
- `idp` (string): External IdP like Google, GitHub, or SAML provider

**Commands:**
- `curl -s 'http://localhost:8080/realms/master/protocol/openid-connect/token' -d 'grant_type=client_credentials&client_id=admin-cli&client_secret=secret' | jq -r '.access_token'`
- `curl -s -X POST 'http://localhost:8080/admin/realms' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{"realm":"acme","enabled":true}' | jq`
- `curl -s 'http://localhost:8080/realms/acme/.well-known/openid-configuration' | jq '.authorization_endpoint, .token_endpoint, .jwks_uri'`
- `curl -s 'http://localhost:8080/realms/acme/protocol/openid-connect/token' -d 'grant_type=password&client_id=web&username=alice&password=secret' | jq '{access_token: (.access_token | length > 0), refresh_expires_in}'`
- `curl -s 'http://localhost:8080/realms/acme/protocol/openid-connect/certs' | jq '.keys[0].kid'`

**Examples:**
- curl -s 'http://localhost:8080/realms/acme/.well-known/openid-configuration' | jq '.authorization_endpoint, .token_endpoint, .jwks_uri'
- curl -s 'http://localhost:8080/realms/acme/protocol/openid-connect/token' -d 'grant_type=password&client_id=web&username=alice&password=secret' | jq -r '.access_token'
- curl -s -X POST 'http://localhost:8080/admin/realms' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{"realm":"acme","enabled":true}' | jq

## References
- [Keycloak Admin REST API](https://www.keycloak.org/docs-api/latest/rest-api/)
- [OIDC Discovery](https://openid.net/specs/openid-connect-discovery-1_0.html)
