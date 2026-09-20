---
name: "same-site-cookie"
description: "Expert reference covering Strict/Lax/None semantics, curl header inspection, server-side Set-Cookie configuration, and CSRF impact analysis. Use when working with samesite config, api or when the user mentions samesite config, api."
---

Expert reference covering Strict/Lax/None semantics, curl header inspection, server-side Set-Cookie configuration, and CSRF impact analysis.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -i -H 'Cookie: session=abc123' https://app.your-app.tes`
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

# SameSite Cookies

Expert skill for SameSite cookie attributes and CSRF defense.

## What this skill does

- Sets Strict, Lax, or None on session cookies server-side
- Inspects Set-Cookie and Cookie headers with curl
- Reasons about CSRF exposure per SameSite value

## When to use

- Hardening session cookies after a CSRF review
- Debugging why cookies are not sent on third-party requests
- Switching to SameSite=None for cross-site embedding

## Real commands

```bash
# What does the server set?
curl -i -H 'Cookie: session=abc123' https://app.your-app.test/me | grep -i 'set-cookie'
curl -i https://app.your-app.test/login -X POST -d 'user=ada&pass=secret' | grep -i set-cookie

# Send a cookie manually and check acceptance
curl -s -o /dev/null -w '%{http_code}\n' https://app.your-app.test/me -b 'session=abc123'

# Model the Set-Cookie header in Python
python -c 'from http.cookies import SimpleCookie; c=SimpleCookie(); c["session"]="abc"; c["session"]["samesite"]="Lax"; c["session"]["secure"]=True; print(c.output())'
```

## Server config

```python
# Flask
response.set_cookie("session", value=tok, samesite="Lax", secure=True, httponly=True)
```

```nginx
# nginx proxy: forward the header untouched
proxy_set_header Cookie $http_cookie;
```

## Semantics

- Strict: never sent on cross-site requests (strongest, worst UX)
- Lax: sent on top-level navigations only (default, safe middle ground)
- None: sent everywhere; requires Secure or browsers reject it

## Testing

```bash
curl -i https://app.your-app.test/me | grep -i set-cookie   # expect samesite=lax; secure
```

## Best practices

- Use Lax by default; Strict only when UX allows
- SameSite=None must pair with Secure on every deployment
- Keep cookies HttpOnly and add CSRF tokens regardless of SameSite

## Capabilities

### samesite-config
Configure and verify SameSite cookie attributes on requests

**Parameters:**
- `samesite_value` (string): Strict, Lax, or None
- `secure` (boolean): Require HTTPS before sending the cookie
- `cookie_name` (string): Name of the session cookie

**Commands:**
- `curl -i -H 'Cookie: session=abc123' https://app.your-app.test/me | grep -i 'set-cookie'`
- `curl -i https://app.your-app.test/login -X POST -d 'user=ada&pass=secret' | grep -i set-cookie`
- `curl -s -o /dev/null -w '%{http_code}\n' https://app.your-app.test/me -b 'session=abc123'`
- `python -c 'from http.cookies import SimpleCookie; c=SimpleCookie(); c["session"]="abc"; c["session"]["samesite"]="Lax"; c["session"]["secure"]=True; print(c.output())'`

**Examples:**
- curl -i https://app.your-app.test/me | grep -i set-cookie
- curl -s -o /dev/null -w '%{http_code}\n' https://app.your-app.test/me -b 'session=abc123; SameSite=Strict'
- python -c 'from http.cookies import SimpleCookie; c=SimpleCookie(); c["s"]="1"; c["s"]["samesite"]="None"; print(c.output())'

## References
- [MDN SameSite cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)
- [OWASP session cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
