---
name: "mtls"
description: "Mutual TLS (mTLS) setup: CA creation, server/client certificates, TLS verification, and enforcing mutual authentication. Use when working with mtls certificates, api or when the user mentions mtls certificates, api."
license: "MIT"
compatibility: "Requires openssl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(openssl:*)"
---

Mutual TLS (mTLS) setup: CA creation, server/client certificates, TLS verification, and enforcing mutual authentication.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -ou`
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

# mTLS

Mutual TLS authenticates both peers: the server presents a cert and the client presents its own, both verified against a shared CA.

## What this skill does

- Generates a CA and issues server/client certificates
- Configures services to require client certificates
- Verifies handshakes and certificate chains

## When to use

- Service-to-service authentication in production
- Replacing API tokens with certificate identity
- Zero-trust network segmentation

## Real commands

```bash
# 1. CA
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 365 -subj "/CN=my-ca"

# 2. Server certificate signed by CA
openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# 3. Client certificate (same flow, CN=client-1)
openssl req -newkey rsa:2048 -nodes -keyout client.key -out client.csr -subj "/CN=client-1"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365

# 4. Verify chain
openssl verify -CAfile ca.crt server.crt client.crt

# 5. Test the handshake
curl --cacert ca.crt --cert client.crt --key client.key https://localhost:8443/api
openssl s_client -connect localhost:8443 -cert client.crt -key client.key -CAfile ca.crt
```

## Server-side enforcement (nginx example)

```nginx
server {
    listen 8443 ssl;
    ssl_certificate     server.crt;
    ssl_certificate_key server.key;
    ssl_client_certificate ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;
}
```

## Best practices

- Keep the CA key offline; issue certs with short lifetimes
- Set `ssl_verify_client optional` during rollout, then `on`
- Verify with `openssl s_client` before wiring clients

## Capabilities

### mtls-certificates
Create a CA and issue server/client certificates, then verify mTLS handshakes with curl and openssl.

**Parameters:**
- `ca_cert` (string): Path to the CA certificate bundle
- `client_cert` (string): Client certificate for mutual auth
- `endpoint` (string): TLS endpoint URL to verify

**Commands:**
- `openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 365 -subj "/CN=my-ca"`
- `openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=localhost"`
- `openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365`
- `curl --cacert ca.crt --cert client.crt --key client.key https://localhost:8443/api`
- `openssl s_client -connect localhost:8443 -cert client.crt -key client.key -CAfile ca.crt`

**Examples:**
- openssl verify -CAfile ca.crt server.crt
- curl -v --cacert ca.crt --cert client.crt --key client.key https://localhost:8443/health
- openssl s_client -connect localhost:8443 -CAfile ca.crt 2>&1 | grep -i 'verify return'

## References
- [OpenSSL man pages](https://www.openssl.org/docs/manmaster/man1/)
- [mTLS Explained (Cloudflare)](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/)
