---
name: "device-auth"
description: "Implements OAuth 2.0 Device Authorization Grant (RFC 8628) on input-constrained devices: device code request, token polling, and slow-down error handling. Use when working with device flow, api or when the user mentions device flow, api."
---

Implements OAuth 2.0 Device Authorization Grant (RFC 8628) on input-constrained devices: device code request, token polling, and slow-down error handling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST https://httpbin.org/anything/oauth/device_autho`
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
