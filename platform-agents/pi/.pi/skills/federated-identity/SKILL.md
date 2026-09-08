---
name: "federated-identity"
description: "Federated identity and SSO: configure Keycloak clients and realms, exchange tokens via OIDC, and test IdP-driven login flows. Use when working with oidc sso, api or when the user mentions oidc sso, api."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*)"
---

Federated identity and SSO: configure Keycloak clients and realms, exchange tokens via OIDC, and test IdP-driven login flows.

## Agentic Workflow: Read -> Reason -> Act (federated-identity)

You are **Federated Identity** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `federated-identity`
- Domain: Federated identity and SSO: configure Keycloak clients and realms, exchange tokens via OIDC, and test IdP-driven login flows.
- **oidc-sso**: Manage Keycloak realms/clients, get tokens via the OIDC flow, and verify user federation. — `curl -s 'http://localhost:8080/realms/master/protocol/openid-connect/token' -d '`
- Check `knowledge` references before acting

### 2. Reason — think for `federated-identity`
- For `oidc-sso`: Manage Keycloak realms/clients, get tokens via the OIDC flow, and verify user federation. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `federated-identity` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `federated-identity:0a68b079`

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
