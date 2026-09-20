---
name: "sso"
description: "Configure single sign-on with Keycloak by creating realms, registering OIDC clients, and exercising token flows from the terminal. Covers kcadm.sh administration, discovery endpoint usage, and logout wiring so SSO sessions terminate cleanly."
---

# Sso

Configure single sign-on with Keycloak by creating realms, registering OIDC clients, and exercising token flows from the terminal. Covers kcadm.sh administration, discovery endpoint usage, and logout wiring so SSO sessions terminate cleanly.

## Instructions

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
