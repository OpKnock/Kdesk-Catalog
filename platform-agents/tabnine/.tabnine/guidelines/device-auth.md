Implements OAuth 2.0 Device Authorization Grant (RFC 8628) on input-constrained devices: device code request, token polling, and slow-down error handling.

## Agentic Workflow: Read -> Reason -> Act (device-auth)

You are **Device Auth** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `device-auth`
- Domain: Implements OAuth 2.0 Device Authorization Grant (RFC 8628) on input-constrained devices: device code request, token polling, and slow-down error handling.
- **device-flow**: Drive the full device code flow with curl: device authorization request, token polling, and error ha — `curl -X POST https://httpbin.org/anything/oauth/device_authorization -d 'client_`
- Check `knowledge` references before acting

### 2. Reason — think for `device-auth`
- For `device-flow`: Drive the full device code flow with curl: device authorization request, token polling, and error handling. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `device-auth` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `device-auth:af56c5de`

# Device Authorization

## What this skill does

OAuth 2.0 Device Authorization Grant (RFC 8628) lets input-constrained devices (smart TVs, CLI logins, IoT) obtain tokens. The device shows a user code and verification URL; the user approves on another device; the client polls for the token.

## When to use

- Adding login to CLIs, TVs, or devices without a browser or keyboard
- Implementing `az login`, `aws sso login` style flows in your own client

## Real commands

```bash
# Step 1: request a device code
curl -s https://httpbin.org/anything/oauth/device_authorization \
  -d 'client_id=MY_CLIENT&scope=openid%20profile' | jq '.device_code, .user_code, .verification_uri_complete'

# Step 2: poll for the token (respect the interval!)  
curl -X POST https://httpbin.org/anything/oauth/token \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=MY_CLIENT' | jq

# Step 3: use and refresh the token
curl -X POST https://httpbin.org/anything/oauth/token -d 'grant_type=refresh_token&refresh_token=REFRESH&client_id=MY_CLIENT' | jq -r '.access_token'
```

## Error handling

```json
{"error": "slow_down"}
{"error": "authorization_pending"}
{"error": "access_denied"}
{"error": "expired_token"}
```

- `authorization_pending`: keep polling after the same interval.
- `slow_down`: increase the interval by 5 seconds before the next poll.
- `expired_token`: the device_code expired; restart the flow.

## Testing

```bash
# Simulate the full flow locally
curl -s https://httpbin.org/anything/oauth/device_authorization -d 'client_id=MY_CLIENT' | jq -r '.verification_uri_complete'
# Open the URL, approve, then poll:
for i in $(seq 1 20); do sleep 5; curl -X POST https://httpbin.org/anything/oauth/token -d "grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=MY_CLIENT" | jq; done
```

## Best practices

- Never log the device_code or access_token.
- Use PKCE (code_challenge) with confidential-client-capable servers even for public clients.
- Implement the `interval` and `slow_down` backoff exactly as specified.

## Capabilities

### device-flow
Drive the full device code flow with curl: device authorization request, token polling, and error handling.

**Parameters:**
- `client-id` (string): Public client identifier registered at the authorization server
- `device-code` (string): Opaque code returned by the device_authorization endpoint, used for polling
- `interval` (integer): Polling interval in seconds returned by the server; increase it on slow_down errors

**Commands:**
- `curl -X POST https://httpbin.org/anything/oauth/device_authorization -d 'client_id=MY_CLIENT&scope=openid%20profile' -H 'Content-Type: application/x-www-form-urlencoded'`
- `curl -X POST https://httpbin.org/anything/oauth/token -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=MY_CLIENT'`
- `curl -X POST https://httpbin.org/anything/oauth/token -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=MY_CLIENT' | jq -r '.access_token'`
- `curl -s https://httpbin.org/anything/oauth/device_authorization -d 'client_id=MY_CLIENT' | jq '.verification_uri_complete'`
- `curl -X POST https://httpbin.org/anything/oauth/token -d 'grant_type=refresh_token&refresh_token=REFRESH&client_id=MY_CLIENT'`

**Examples:**
- curl -s https://httpbin.org/anything/oauth/device_authorization -d 'client_id=MY_CLIENT' | jq '.device_code, .user_code, .verification_uri_complete'
- curl -X POST https://httpbin.org/anything/oauth/token -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=MY_CLIENT' | jq
- curl -X POST https://httpbin.org/anything/oauth/token -d 'grant_type=refresh_token&refresh_token=REFRESH&client_id=MY_CLIENT' | jq -r '.access_token'

## References
- [RFC 8628 Device Authorization Grant](https://www.rfc-editor.org/rfc/rfc8628.html)