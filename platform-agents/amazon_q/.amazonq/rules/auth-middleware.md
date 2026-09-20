# Auth Middleware

Implements authentication middleware: JWT verification with jsonwebtoken, Passport strategies, oauth2-proxy for edge auth, and token lifecycle checks.

## Instructions

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