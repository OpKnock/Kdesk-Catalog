---
name: "Encryption In Transit"
description: "TLS encryption in transit: test certificates with openssl s_client, inspect cipher suites and handshakes, and verify proper SNI and chain validation. Use when working with tls verification, api or when the user mentions tls verification, api."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh"]
alwaysApply: false
---

TLS encryption in transit: test certificates with openssl s_client, inspect cipher suites and handshakes, and verify proper SNI and chain validation.

## Agentic Workflow: Read -> Reason -> Act (encryption-in-transit)

You are **Encryption In Transit** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `encryption-in-transit`
- Domain: TLS encryption in transit: test certificates with openssl s_client, inspect cipher suites and handshakes, and verify proper SNI and chain validation.
- **tls-verification**: Probe TLS endpoints, inspect certificates and ciphers, and validate chains. — `echo | openssl s_client -connect httpbin.org:443 -servername httpbin.org 2>/dev/`
- Check `knowledge` and `prerequisites: echo, nmap`

### 2. Reason — think for `encryption-in-transit`
- For `tls-verification`: Probe TLS endpoints, inspect certificates and ciphers, and validate chains. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `encryption-in-transit` tools
- Tools: `Glob`, `Grep`, `Read`, `Echo`, `Nmap` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `encryption-in-transit:de6a67b6`

# Encryption in Transit

## What this skill does

Encryption in transit means every byte between client and server is protected by TLS. This skill focuses on verifying that protection: certificate validity, protocol versions, cipher suites, chain trust, and HSTS.

## When to use

- Diagnosing certificate expiry or chain errors
- Auditing cipher and TLS version support
- Verifying SNI serves the right certificate

## Real commands

```bash
# Certificate dates, subject, issuer
 echo | openssl s_client -connect httpbin.org:443 -servername httpbin.org 2>/dev/null | openssl x509 -noout -dates -subject -issuer

# TLS version and negotiated cipher
 echo | openssl s_client -connect api.github.com:443 -tls1_3 2>/dev/null | grep -E 'Protocol|Cipher'

# Strict chain validation
 echo | openssl s_client -connect httpbin.org:443 -verify_return_error 2>&1 | grep -iE 'verify|error'

# Enumerate supported ciphers
 nmap --script ssl-enum-ciphers -p 443 httpbin.org

# HSTS presence
 curl -sI https://httpbin.org | grep -i 'strict-transport-security'
```

## Chain debugging

```bash
# Print the full chain presented by the server
 echo | openssl s_client -connect httpbin.org:443 -showcerts 2>/dev/null | grep -E '^\s+i:|^s:' | head -20
```

## Hardening config example (nginx)

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## Best practices

- Disable TLS 1.0/1.1; require 1.2 minimum.
- Set HSTS before deploying HTTPS so browsers never downgrade.
- Automate certificate renewal monitoring (e.g. expiry alerts 30 days out).
- Always pass `-servername` when testing virtual-hosted endpoints.

## Capabilities

### tls-verification
Probe TLS endpoints, inspect certificates and ciphers, and validate chains.

**Parameters:**
- `host` (string): Hostname of the TLS endpoint
- `port` (integer): TLS port, usually 443
- `sni-host` (string): SNI name for virtual-hosted endpoints

**Commands:**
- `echo | openssl s_client -connect httpbin.org:443 -servername httpbin.org 2>/dev/null | openssl x509 -noout -dates -subject -issuer`
- `echo | openssl s_client -connect api.github.com:443 -tls1_3 2>/dev/null | grep -E 'Protocol|Cipher'`
- `echo | openssl s_client -connect httpbin.org:443 -verify_return_error 2>&1 | grep -iE 'verify|error'`
- `nmap --script ssl-enum-ciphers -p 443 httpbin.org`
- `curl -sI https://httpbin.org | grep -i 'strict-transport-security'`

**Examples:**
- echo | openssl s_client -connect httpbin.org:443 -servername httpbin.org 2>/dev/null | openssl x509 -noout -dates -subject -issuer
- echo | openssl s_client -connect api.github.com:443 -tls1_3 2>/dev/null | grep -E 'Protocol|Cipher'
- curl -sI https://httpbin.org | grep -i 'strict-transport-security'

## References
- [openssl s_client man page](https://docs.openssl.org/master/man1/openssl-s_client/)