---
trigger: glob
description: "Designs OAuth2/OpenID Connect flows: token endpoints, PKCE, scopes, and Keycloak realm administration. Use when working with oauth2c, keycloak or when the user mentions oauth2c, keycloak."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Designs OAuth2/OpenID Connect flows: token endpoints, PKCE, scopes, and Keycloak realm administration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `oauth2c auth-code --issuer http://localhost:8080 --client-id`, `kcadm.sh config credentials --server http://localhost:8080 -`
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

**Parameters:**
- `issuer` (string): OIDC issuer URL
- `client-id` (string): OAuth client id
- `pkce` (string): Use PKCE for the flow

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

**Parameters:**
- `realm` (string): Keycloak realm
- `clientId` (string): Client identifier
- `server` (string): Keycloak server URL

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

## References
- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [oauth2c](https://github.com/cloudentity/oauth2c)
- [Keycloak Admin CLI](https://www.keycloak.org/docs/latest/server_admin/index.html)
