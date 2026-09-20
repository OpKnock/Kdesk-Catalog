---
name: "Session Management"
description: "Manages HTTP session lifecycles with Redis-backed storage. Creates server-side session records with TTL, drives cookie lifecycle through login and logout flows, and enforces immediate invalidation on logout by deleting the Redis record."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Session Management

Manages HTTP session lifecycles with Redis-backed storage. Creates server-side session records with TTL, drives cookie lifecycle through login and logout flows, and enforces immediate invalidation on logout by deleting the Redis record.

## Instructions

# Session Management

Hand-crafted skill for HTTP session lifecycles with Redis storage.

## What this skill does

- Stores session state server-side with TTLs
- Drives the cookie lifecycle with curl: login, use, logout
- Invalidates sessions on logout and enforces expiry

## When to use

- Designing auth state for a new web app
- Debugging why sessions persist after logout
- Tuning session timeout policy

## Real commands

```bash
# Create a session record with 1h TTL
redis-cli SET session:7f3a '{"uid":42,"role":"admin"}' EX 3600
redis-cli TTL session:7f3a

# Login: server sets the cookie in cookies.txt
curl -i -c cookies.txt -X POST http://localhost:8080/login -d 'user=ada'

# Authenticated request with the cookie jar
curl -i -b cookies.txt http://localhost:8080/me

# Logout: server must delete the session record
curl -X POST -b cookies.txt http://localhost:8080/logout
redis-cli EXISTS session:7f3a   # should return 0
```

## Cookie attributes

- HttpOnly, Secure, SameSite=Lax
- Session ID: 128+ random bits from a CSPRNG

## Testing

```bash
curl -i -c cookies.txt -X POST http://localhost:8080/login -d 'user=ada'   # Set-Cookie present
redis-cli TTL session:7f3a
curl -i -b cookies.txt http://localhost:8080/me                            # 200
curl -X POST -b cookies.txt http://localhost:8080/logout
redis-cli EXISTS session:7f3a                                              # 0
```

## Best practices

- Store only the session ID in the cookie; state lives server-side
- Slide expiry on activity, hard-expire after N hours
- On logout, delete the Redis record immediately, not just the cookie

## Capabilities

### session-lifecycle
Manages HTTP session lifecycles with Redis-backed storage. Creates server-side session records with TTL, drives cookie lifecycle through login and logout flows, and enforces immediate invalidation on logout by deleting the Redis record.

**Commands:**
- `redis-cli SET session:abc123 "{\"user_id\":42}" EX 3600`
- `redis-cli GET session:abc123`
- `redis-cli EXPIRE session:abc123 7200`
- `redis-cli DEL session:abc123`
- `curl -b "session_id=abc123" http://api.example.org/protected`

**Examples:**
- redis-cli SET session:abc123 "{\"user_id\":42}" EX 3600
- curl -b "session_id=abc123" http://api.example.org/protected
- redis-cli DEL session:abc123