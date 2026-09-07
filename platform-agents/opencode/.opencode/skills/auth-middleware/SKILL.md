---
name: "auth-middleware"
description: "Implements authentication middleware: JWT verification with jsonwebtoken, Passport strategies, oauth2-proxy for edge auth, and token lifecycle checks. Use when working with jwt middleware, passport oauth, backend or when the user mentions jwt middleware, passport oauth, backend."
---

Implements authentication middleware: JWT verification with jsonwebtoken, Passport strategies, oauth2-proxy for edge auth, and token lifecycle checks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install jsonwebtoken express`, `npm install passport passport-jwt`
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

# Auth Middleware

Authentication middleware implementation.

## What This Skill Does
- Verifies JWTs on requests
- Extracts user context from tokens
- Rejects missing/expired credentials

## When to Use
- Protecting API routes
- Adding SSO with oauth2-proxy
- Standardizing auth across services

## Real Commands

```bash
npm install jsonwebtoken express
node -e "const jwt=require('jsonwebtoken'); const t=jwt.sign({sub:'user-1'},'s3cret',{expiresIn:'1h'}); console.log(t)"
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/me
```

## Middleware Example

```js
function requireAuth(req, res, next) {
  const header = req.get('Authorization') || '';
  const token = header.replace('Bearer ', '');
  try {
    req.user = jwt.verify(token, SECRET);
    next();
  } catch {
    res.sendStatus(401);
  }
}
```

## Testing
- Test missing, invalid, and expired tokens
- Verify user context on protected routes
- Test role-based access paths


## Best Practices
- Always verify expiry and signature
- Use RS256 for production issuance
- Return 401 uniformly for auth failures

## Capabilities

### jwt-middleware
Verify JWTs in request middleware

**Parameters:**
- `secret` (string): JWT signing secret
- `expiresIn` (string): Token lifetime
- `claims` (object): Token claims

**Commands:**
- `npm install jsonwebtoken express`
- `node -e "const jwt=require('jsonwebtoken'); const t=jwt.sign({sub:'user-1',role:'admin'},'s3cret',{expiresIn:'1h'}); console.log(t)"`
- `node -e "const jwt=require('jsonwebtoken'); const t=jwt.sign({sub:'user-1'},'s3cret',{expiresIn:5}); setTimeout(()=>{try{jwt.verify(t,'s3cret')}catch(e){console.log('expired:',e.name)}},6000)"`
- `curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/me`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/me`

**Examples:**
- jwt.sign issues tokens with claims
- jwt.verify validates signature and expiry
- curl with/without tokens tests enforcement

### passport-oauth
Authenticate with Passport and oauth2-proxy

**Commands:**
- `npm install passport passport-jwt`
- `node -e "const p=require('passport'); console.log(typeof p.authenticate)"`
- `docker run -d -p 4180:4180 bitnami/oauth2-proxy --provider github --upstream http://localhost:3000 --email-domain example.com --client-id $CLIENT_ID --client-secret $CLIENT_SECRET`
- `curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer invalid" http://localhost:4180/oauth2/start`

**Examples:**
- general-cli --help
- general-api --help

## References
- [Passport.js Docs](https://www.passportjs.org/docs/)
- [oauth2-proxy Docs](https://oauth2-proxy.github.io/oauth2-proxy/)
