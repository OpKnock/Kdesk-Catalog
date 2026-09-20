---
name: "identity-provider"
description: "Identity provider operations with Keycloak: kcadm.sh realm and user administration, OIDC discovery, client registration, and token introspection."
---

# Identity Provider

Identity provider operations with Keycloak: kcadm.sh realm and user administration, OIDC discovery, client registration, and token introspection.

## Instructions

# Identity Provider

Run and administer a Keycloak-based identity provider.

## What this skill does

- Configures kcadm.sh credentials and manages realms.
- Creates and queries users and clients.
- Verifies OIDC discovery metadata.
- Introspects tokens for debugging.

## When to use

- Standing up SSO for a new environment.
- Provisioning a test user or client programmatically.
- Debugging OIDC flows against a real IdP.

## Real commands

```bash
# Login once per session
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# Realms
kcadm.sh get realms
kcadm.sh create realms -s realm=myrealm -s enabled=true

# Users
kcadm.sh create users -r myrealm -s username=alice -s enabled=true -p
kcadm.sh get users -r myrealm --query email=alice@example.com
kcadm.sh update users/<id> -r myrealm -s 'email=alice@example.com'

# Clients
kcadm.sh get clients -r myrealm
kcadm.sh create clients -r myrealm -s clientId=webapp -s publicClient=true

# OIDC discovery
curl http://localhost:8080/realms/myrealm/.well-known/openid-configuration | jq '.authorization_endpoint, .token_endpoint'
```

## Token exchange for testing

```bash
TOKEN=$(curl -s -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token \
  -d client_id=webapp -d username=alice -d password=pass -d grant_type=password | jq -r .access_token)
curl -s http://localhost:8080/realms/myrealm/protocol/openid-connect/userinfo -H "Authorization: Bearer $TOKEN"
```

## Testing

```bash
kcadm.sh get realms -r myrealm | jq '.realm, .enabled'
```

## Best practices

- Never use password grant in production; use authorization code + PKCE.
- Scope kcadm.sh tokens to a service account, not the master admin.
- Version realm config: export with `kcadm.sh get realms -r myrealm --export` for drift checks.
- Rotate client secrets and revoke tokens via `kcadm.sh logout` when needed.

## Example exchange

```
User: Create realm myrealm with user alice.
Agent: kcadm.sh config credentials ... ; kcadm.sh create realms -s realm=myrealm -s enabled=true
       kcadm.sh create users -r myrealm -s username=alice -s enabled=true -p
```

## Capabilities

### keycloak-admin
Administer Keycloak realms, users, and clients from the CLI.

**Commands:**
- `kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin`
- `kcadm.sh get realms`
- `kcadm.sh create users -r myrealm -s username=alice -s enabled=true -p`
- `kcadm.sh get clients -r myrealm`
- `curl http://localhost:8080/realms/myrealm/.well-known/openid-configuration`

**Examples:**
- kcadm.sh create realms -s realm=myrealm -s enabled=true
- kcadm.sh update users/6c1d -r myrealm -s 'email=alice@example.com'
- kcadm.sh get users -r myrealm --query email=alice@example.com
