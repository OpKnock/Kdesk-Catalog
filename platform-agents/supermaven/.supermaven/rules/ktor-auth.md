# Ktor Auth

Secure Ktor applications: JWT bearer validation, Basic auth, session auth, and protected-route testing with curl.

## Instructions

# Ktor Auth

Protect Ktor routes with JWT, Basic, and session authentication.

## What this skill does

- Adds JWT bearer validation with HS256/RS256 keys.
- Adds Basic auth for simple service credentials.
- Tests 401/200 behavior with curl.

## When to use

- Securing Ktor APIs behind bearer tokens.
- Service-to-service auth with Basic headers.
- Adding claims-based authorization (roles in JWT).

## Real commands

```bash
# Run the app
./gradlew run

# Unauthenticated request -> 401
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/me

# With a valid token
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8080/me | jq .

# Basic auth
curl -s -u alice:password http://localhost:8080/basic
curl -s -o /dev/null -w '%{http_code}\n' -u alice:wrong http://localhost:8080/basic

# Basic header from base64
curl -s -H 'Authorization: Basic YWxpY2U6cGFzc3dvcmQ=' http://localhost:8080/basic
```

## JWT config example

```kotlin
install(Authentication) {
    jwt("auth-jwt") {
        realm = "ktor.io"
        verifier(
            JWT.verifier(JWKProvider("https://example.com/.well-known/jwks.json"))
        )
        validate { credential ->
            if (credential.payload.getClaim("role").asString() == "admin")
                JWTPrincipal(credential.payload) else null
        }
    }
}

routing {
    authenticate("auth-jwt") {
        get("/me") { call.respond(User("alice", "admin")) }
    }
}
```

## Testing

```bash
./gradlew test
```

## Best practices

- Verify signature AND claims (exp, iss, aud) in the validate block.
- Use JWK providers for RS256; rotate secrets without redeploys.
- Return 401 for missing/invalid, 403 for valid-but-forbidden.

## Capabilities

### jwt-auth
Configure and test JWT authentication in Ktor.

**Commands:**
- `./gradlew run`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/me`
- `curl -s -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbGljZSJ9.signature' http://localhost:8080/me`
- `curl -s -H 'Authorization: Bearer $TOKEN' http://localhost:8080/me | jq .`

**Examples:**
- curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/me
- curl -s -H 'Authorization: Bearer $TOKEN' http://localhost:8080/me
- ./gradlew run

### basic-auth
Configure Basic auth and test credentials via curl.

**Commands:**
- `curl -s -u alice:password http://localhost:8080/basic`
- `curl -s -o /dev/null -w '%{http_code}\n' -u alice:wrong http://localhost:8080/basic`
- `curl -s -H 'Authorization: Basic YWxpY2U6cGFzc3dvcmQ=' http://localhost:8080/basic`
- `./gradlew test`

**Examples:**
- curl -s -u alice:password http://localhost:8080/basic
- curl -s -o /dev/null -w '%{http_code}\n' -u alice:wrong http://localhost:8080/basic
- ./gradlew test