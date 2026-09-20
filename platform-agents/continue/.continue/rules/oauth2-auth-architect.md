---
name: "oauth2-auth-architect"
description: "Designs OAuth2/OpenID Connect flows: token endpoints, PKCE, scopes, and Keycloak realm administration."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# oauth2-auth-architect

Designs OAuth2/OpenID Connect flows: token endpoints, PKCE, scopes, and Keycloak realm administration.

## Instructions

# OAuth2 Architecture

Design and verify OAuth2/OIDC integrations.

## When to Use

- Adding SSO to an app
- Migrating to OIDC providers
- Auditing token flows and scopes

## Flow selection

- Authorization Code + PKCE: browser apps.
- Client Credentials: machine-to-machine.
- Refresh Token: long-lived sessions.
- Device: TVs/CLI apps.

## Test with oauth2c

```bash
oauth2c auth-code --issuer https://issuer.example.com --client-id web --pkce --scopes openid,email
oauth2c client-credentials --issuer https://issuer.example.com --client-id svc --client-secret $SECRET
```

## Keycloak administration

```bash
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password $KC_PASS
kcadm.sh create clients -r my-realm -s clientId=web-app -s publicClient=true
kcadm.sh create users -r my-realm -s username=ada -s enabled=true
```

## Security checklist

- PKCE mandatory for public clients.
- Short access tokens, rotated refresh tokens.
- Least-privilege scopes; audit scope requests.
- Validate issuer and audience on every token.

## Best practices

- Never log tokens or authorization codes.
- Store client secrets in a vault, not config.
- Rotate JWKS and keys on a schedule.
- Test expiry/refresh behavior in integration tests.

## Testing

```bash
oauth2c auth-code --issuer ... --client-id web --pkce --scopes openid
curl -I -H "Authorization: Bearer $TOKEN" https://api/resource
```

Verify 401 on expired and wrong-audience tokens.

## Capabilities

### oauth2c
Exercise OAuth2 flows end-to-end with oauth2c.

**Commands:**
- `oauth2c auth-code --issuer http://localhost:8080 --client-id my-client --client-secret secret --scopes openid,email`
- `oauth2c client-credentials --issuer http://localhost:8080 --client-id svc --client-secret secret`
- `oauth2c refresh-token --issuer http://localhost:8080 --client-id my-client --client-secret secret --refresh-token TOKEN`
- `oauth2c auth-code --issuer http://localhost:8080 --client-id my-client --pkce --scopes openid`
- `oauth2c device --issuer http://localhost:8080 --client-id tv-client`

**Examples:**
- oauth2c client-credentials --issuer http://localhost:8080 --client-id svc --client-secret $SECRET | jq '.access_token'
- oauth2c auth-code --issuer http://localhost:8080 --client-id web --pkce --scopes openid,profile
- oauth2c auth-code --issuer http://localhost:8080 --client-id web --client-secret secret --response-mode form_post

### keycloak
Administer Keycloak realms, clients, and users.

**Commands:**
- `kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin`
- `kcadm.sh get realms`
- `kcadm.sh create clients -r my-realm -f client.json`
- `kcadm.sh create users -r my-realm -s username=ada -s enabled=true -p '{"type":"password","value":"S3cret!"}'`
- `kcadm.sh get clients -r my-realm --fields id,clientId | head -30`

**Examples:**
- kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password $KC_PASS
- kcadm.sh create clients -r my-realm -s clientId=web-app -s publicClient=true
- kcadm.sh get users -r my-realm -q username=ada