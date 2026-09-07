---
name: "sso"
description: "Configure single sign-on with Keycloak by creating realms, registering OIDC clients, and exercising token flows from the terminal. Covers kcadm.sh administration, discovery endpoint usage, and logout wiring so SSO sessions terminate cleanly. Use when working with keycloak sso, api or when the user mentions keycloak sso, api."
---

Configure single sign-on with Keycloak by creating realms, registering OIDC clients, and exercising token flows from the terminal. Covers kcadm.sh administration, discovery endpoint usage, and logout wiring so SSO sessions terminate cleanly.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kcadm.sh config credentials --server http://localhost:8080 -`
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

# SSO with Keycloak

Hand-crafted skill for single sign-on with Keycloak.

## What this skill does

- Creates realms and clients with kcadm.sh
- Exercises OIDC token flows against the token endpoint
- Uses discovery for endpoints and logout wiring

## When to use

- Standing up SSO for internal apps
- Testing flows before writing app code
- Auditing clients and their scopes

## Real commands

```bash
# Authenticate the admin CLI
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# Create a realm
kcadm.sh create realms -s realm=myrealm -s enabled=true

# Create a client from JSON
kcadm.sh create clients -r myrealm -f client.json

# Password grant token
curl -s -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token -d 'grant_type=password&client_id=app&username=ada&password=secret' | jq -r .access_token

# Discovery
curl -s http://localhost:8080/realms/myrealm/.well-known/openid-configuration | jq -r '.end_session_endpoint'
```

## client.json

```json
{
  "clientId": "app",
  "enabled": true,
  "publicClient": true,
  "redirectUris": ["http://localhost:3000/cb"],
  "directAccessGrantsEnabled": true
}
```

## Testing

```bash
TOKEN=$(curl -s -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token -d 'grant_type=password&client_id=app&username=ada&password=secret' | jq -r .access_token)
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8080/realms/myrealm/protocol/openid-connect/userinfo | jq
```

## Best practices

- Prefer authorization_code for browser apps; keep secrets server-side
- Rotate client secrets and disable direct access grants in prod
- Wire end_session_endpoint into logout so SSO sessions die too

## Capabilities

### keycloak-sso
Configure SSO with Keycloak: realms, clients, token flows

**Parameters:**
- `realm` (string): Keycloak realm name
- `client_id` (string): OIDC client identifier
- `grant_type` (string): authorization_code, password, client_credentials, refresh_token

**Commands:**
- `kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin`
- `kcadm.sh create realms -s realm=myrealm -s enabled=true`
- `kcadm.sh create clients -r myrealm -f client.json`
- `curl -s -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token -d 'grant_type=password&client_id=app&username=ada&password=secret' | jq -r .access_token`
- `curl -s http://localhost:8080/realms/myrealm/.well-known/openid-configuration | jq -r '.end_session_endpoint'`

**Examples:**
- kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin
- kcadm.sh create clients -r myrealm -f client.json
- curl -s -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token -d 'grant_type=password&client_id=app&username=ada&password=secret' | jq -r .access_token

## References
- [Keycloak server admin guide](https://www.keycloak.org/docs/latest/server_admin/index.html)
- [Keycloak Admin CLI](https://www.keycloak.org/docs/latest/server_admin/index.html#admin-cli)
