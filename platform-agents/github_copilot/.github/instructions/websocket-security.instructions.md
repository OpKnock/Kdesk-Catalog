---
applyTo: "**/*.r **/*.rs **/*.sh"
---

# Websocket Security

Hardens WebSocket endpoints against hijacking and abuse. Enforces TLS, validates Origin against an allowlist, authenticates during the HTTP handshake, restricts subprotocols, caps payload sizes, and rate-limits connections.

## Instructions

# WebSocket Security

## What this skill does

Secure WebSocket endpoints against hijacking, cross-site attacks, and abuse: enforce TLS, validate Origin, authenticate during the handshake, restrict subprotocols, and cap payload sizes.

## When to use

- Exposing WebSockets to untrusted clients
- Auditing an existing socket endpoint
- Fixing CSWSH (cross-site WebSocket hijacking)

## Real commands

```bash
# Authenticated connection
wscat -c wss://api.your-app.test/socket -H "Authorization: Bearer token123"

# Malicious origin must be rejected (expect handshake failure)
wscat -c wss://api.your-app.test/socket -H "Origin: https://evil.com"

# Raw upgrade request without proper handshake
curl -s -X POST http://localhost:8080/socket \
  -H "Upgrade: websocket" -H "Connection: Upgrade" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -o /dev/null -w "%{http_code}\n"

# Oversized frame should be rejected
wscat -c ws://localhost:8080/socket -x "{\"size\":\"10MB"}"
```

## Hardening checklist

- TLS only: reject ws:// in production
- Validate Origin against a strict allowlist
- Authenticate in the HTTP handshake, not after connect
- Allowlist subprotocols; never echo unknown ones
- Enforce max frame and message sizes
- Rate-limit connections per IP and per token

## Best practices

- Never trust Origin alone; combine with tokens
- Rotate socket tokens; keep them short-lived
- Log auth failures without leaking credentials
- Close connections that violate limits

## Testing

```bash
wscat -c ws://localhost:8080/socket -H "Origin: https://evil.com" 2>&1 | head -3
curl -s http://localhost:8080/socket/status | jq ".authRequired"
```

## Capabilities

### ws-security
Harden and audit WebSocket endpoints

**Commands:**
- `wscat -c wss://api.your-app.test/socket -H "Authorization: Bearer token123"`
- `wscat -c wss://api.your-app.test/socket -H "Origin: https://evil.com"`
- `curl -s -X POST http://localhost:8080/socket -H "Upgrade: websocket" -H "Connection: Upgrade" -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" -o /dev/null -w "%{http_code}\n"`
- `wscat -c ws://localhost:8080/socket -x "{\"size\":\"10MB"}"`
- `curl -s http://localhost:8080/socket/status | jq ".authRequired"`

**Examples:**
- wscat -c wss://api.your-app.test/socket -H "Origin: https://api.your-app.test" -H "Authorization: Bearer token123"
- curl -s -X POST http://localhost:8080/socket -H "Upgrade: websocket" -H "Connection: Upgrade" -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" -H "Origin: http://localhost" -o /dev/null -w "%{http_code}\n"
- wscat -c wss://api.your-app.test/socket -x "{\"hello\":1}" --wait 2
