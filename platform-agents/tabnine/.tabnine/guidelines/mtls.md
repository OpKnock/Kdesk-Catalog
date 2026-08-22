# Mtls

Mutual TLS (mTLS) setup: CA creation, server/client certificates, TLS verification, and enforcing mutual authentication.

## Instructions

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