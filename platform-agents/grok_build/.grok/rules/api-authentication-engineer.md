Implements API authentication: JWT issuance and validation, OAuth 2.0 flows, API keys, and mTLS with rotation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install jsonwebtoken`, `npm install openid-client`
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

# API Authentication Engineer

Implements authentication for APIs: JWTs, OAuth 2.0, API keys, and mTLS.

## When to Use
- Adding auth to an API
- Implementing OAuth client flows
- Securing service-to-service calls

## Real Commands

```bash
# JWT
npm install jsonwebtoken
jwt decode $(node -e "const j=require('jsonwebtoken');console.log(j.sign({sub:'u1'},'secret',{expiresIn:'1h'}))") 2>/dev/null || node -e "const j=require('jsonwebtoken');console.log(j.verify(j.sign({sub:'u1'},'secret',{expiresIn:'1h'}),'secret'))"

# Keycloak client
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin
kcadm.sh create clients -r demo -s clientId=api-client -s secret=change-me

# Client credentials token
curl -s -X POST http://localhost:8080/realms/demo/protocol/openid-connect/token -d 'grant_type=client_credentials&client_id=api-client&client_secret=change-me'

# mTLS certs
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```

## Token Design
- Short-lived access tokens (15m)
- Refresh tokens with rotation
- Audience and scope claims enforced

## Testing
Verify expired tokens are rejected and scopes are enforced per route.

## Best Practices
- Rotate signing keys on a schedule
- Never log tokens or secrets

## Capabilities

### jwt-implementation
Issue, validate, and rotate JWTs for API access

**Parameters:**
- `audience` (string): Token audience
- `expiry` (string): Token lifetime

**Commands:**
- `npm install jsonwebtoken`
- `node -e "const j=require('jsonwebtoken');const t=j.sign({sub:'u1',scope:'read'},'secret',{expiresIn:'1h'});console.log(t)"`
- `node -e "const j=require('jsonwebtoken');const t=j.sign({sub:'u1'},'secret',{expiresIn:'1h'});console.log(j.verify(t,'secret'))"`
- `jwt decode $(node -e "const j=require('jsonwebtoken');console.log(j.sign({sub:'u1'},'secret',{expiresIn:'1h'}))")`
- `node -e "const j=require('jsonwebtoken');try{j.verify('bad.token.here','secret')}catch(e){console.log(e.message)}"`

**Examples:**
- jwt decode $(node -e "const j=require('jsonwebtoken');console.log(j.sign({sub:'u1'},'secret',{expiresIn:'1h'}))")
- node -e "const j=require('jsonwebtoken');const t=j.sign({sub:'u1'},'secret',{expiresIn:'1h'});setTimeout(()=>{try{j.verify(t,'secret');console.log('ok')}catch(e){console.log('expired')}},2000)"
- node -e "const j=require('jsonwebtoken');console.log(j.sign({sub:'u1'},'secret',{expiresIn:'15m',aud:'api'}) && 'token issued')"

### oauth2-flows
Configure OAuth 2.0 authorization code and client credentials flows

**Parameters:**
- `issuer` (string): OIDC issuer URL
- `clientId` (string): OAuth client ID

**Commands:**
- `npm install openid-client`
- `node -e "const {Issuer}=require('openid-client');Issuer.discover('http://localhost:8080/.well-known/openid-configuration').then(i=>console.log(i.metadata.token_endpoint))"`
- `kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin`
- `kcadm.sh create clients -r demo -s clientId=api-client -s publicClient=false -s secret=change-me`
- `curl -s -X POST http://localhost:8080/realms/demo/protocol/openid-connect/token -d 'grant_type=client_credentials&client_id=api-client&client_secret=change-me'`

**Examples:**
- node -e "const {Issuer}=require('openid-client');Issuer.discover('http://localhost:8080/.well-known/openid-configuration').then(i=>console.log(i.metadata.token_endpoint))"
- kcadm.sh create clients -r demo -s clientId=api-client -s secret=change-me
- curl -s -X POST http://localhost:8080/realms/demo/protocol/openid-connect/token -d 'grant_type=client_credentials&client_id=api-client&client_secret=change-me'

## References
- [JWT Introduction](https://jwt.io/introduction)
- [OAuth 2.0](https://oauth.net/2/)
- [Keycloak Admin CLI](https://www.keycloak.org/docs/latest/server_admin/)