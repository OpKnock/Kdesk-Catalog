---
name: "api-auth-mtls"
description: "API auth with mutual TLS (mTLS) - generate CA and client certificates with openssl, configure the server, and test mTLS handshakes."
---

# Api Auth mTLS

API auth with mutual TLS (mTLS) - generate CA and client certificates with openssl, configure the server, and test mTLS handshakes.

## Instructions

# API Auth (mTLS)

## What this skill does
Authenticate API clients with mutual TLS: create a CA, issue client certificates, configure the server to require client certs, and verify handshakes with curl and openssl.

## When to use
- Server-to-server auth between high-value services
- Replacing shared secrets for internal APIs
- Zero-trust API access

## Real commands
```bash
# Create a CA
openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt \
  -days 365 -nodes -subj '/CN=Demo CA'

# Create a client key + CSR
openssl req -newkey rsa:2048 -keyout client.key -out client.csr \
  -nodes -subj '/CN=partner-1'

# Sign the client certificate
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 180

# Verify the handshake with client auth
openssl s_client -connect localhost:8443 -cert client.crt -key client.key -CAfile ca.crt -brief

# Call the API with mTLS
curl -s --cert client.crt --key client.key --cacert ca.crt \
  https://localhost:8443/api/data -o /dev/null -w '%{http_code}\n'

# No client cert: handshake should fail
openssl s_client -connect localhost:8443 -CAfile ca.crt -brief 2>&1 | grep -i 'no peer certificate'
```

## Server config (nginx snippet)
```nginx
server {
  listen 8443 ssl;
  ssl_certificate     /etc/tls/server.crt;
  ssl_certificate_key /etc/tls/server.key;
  ssl_client_certificate /etc/tls/ca.crt;
  ssl_verify_client on;
}
```

## Best practices
- Short certificate lifetimes (90-180 days) with auto-renewal
- Use SAN/SPIFFE identities, not CN-only
- CRL or OCSP for revocation
- Keep the CA key offline

## Testing
```bash
curl -s --cert client.crt --key client.key --cacert ca.crt https://localhost:8443/api/data
curl -s --cacert ca.crt https://localhost:8443/api/data -o /dev/null -w '%{http_code}\n'  # expect failure
```

## Capabilities

### mtls-auth
Set up and verify mutual TLS authentication

**Commands:**
- `openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -days 365 -nodes -subj '/CN=Demo CA'`
- `openssl req -newkey rsa:2048 -keyout client.key -out client.csr -nodes -subj '/CN=partner-1'`
- `openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 180`
- `curl -s --cert client.crt --key client.key --cacert ca.crt https://localhost:8443/api/data -o /dev/null -w '%{http_code}'`
- `openssl s_client -connect localhost:8443 -cert client.crt -key client.key -CAfile ca.crt -brief`

**Examples:**
- openssl req -newkey rsa:2048 -keyout client.key -out client.csr -nodes -subj '/CN=partner-1/O=Acme' -addext 'subjectAltName=URI:spiffe://demo/acme/partner-1'
- curl -s --cert client.crt --key client.key --cacert ca.crt https://localhost:8443/api/data | jq '.client_cn'
- openssl s_client -connect localhost:8443 -CAfile ca.crt -brief 2>&1 | grep -i 'no peer certificate'
