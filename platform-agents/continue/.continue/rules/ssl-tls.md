---
name: "ssl-tls"
description: "Inspects, validates, and troubleshoots TLS certificates and handshakes with openssl, sslscan, and certbot."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

# ssl-tls

Inspects, validates, and troubleshoots TLS certificates and handshakes with openssl, sslscan, and certbot.

## Instructions

# SSL/TLS

Inspect, validate, and troubleshoot TLS certificates and handshakes.

## What This Skill Does

- Reads certificates and verifies chains with openssl
- Tests live handshakes and ciphers against servers
- Generates CSRs and self-signed certificates
- Automates Let's Encrypt issuance and renewal with certbot

## When to Use

- A certificate fails validation or is about to expire
- Checking which ciphers a server supports
- Generating local test certificates

## Real Commands

```bash
# Inspect a live cert
openssl s_client -connect example.com:443 -servername example.com -showcerts
openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates

# Local cert inspection
openssl x509 -in cert.pem -text -noout
openssl verify -CAfile ca-bundle.pem server.pem

# Generate a CSR and self-signed cert
openssl req -new -newkey rsa:2048 -nodes -keyout key.pem -out csr.pem
openssl req -x509 -newkey rsa:2048 -nodes -days 365 -keyout key.pem -out cert.pem

# Cipher support
sslscan example.com
nmap --script ssl-enum-ciphers -p 443 example.com

# Let's Encrypt
certbot certonly --standalone -d example.com
certbot renew --dry-run
```

## Best Practices

- Verify expiry via monitoring; alerts 30 days before renewal
- Serve full chain; verify with openssl verify -CAfile
- Disable TLS 1.0/1.1 and weak ciphers
- Test renewals with certbot renew --dry-run after config changes
- Use key size 2048+ and pin via SRI/HSTS headers

## Capabilities

### certificate-inspection
Inspect certificates, chains, and server handshakes.

**Commands:**
- `openssl s_client -connect localhost:443 -servername localhost -showcerts`
- `openssl x509 -in cert.pem -text -noout`
- `openssl x509 -in cert.pem -dates -issuer -subject`
- `openssl s_client -connect localhost:443 -servername localhost 2>/dev/null | openssl x509 -noout -dates`
- `openssl verify -CAfile ca-bundle.pem cert.pem`

**Examples:**
- openssl s_client -connect localhost:443 -servername localhost | openssl x509 -noout -subject -issuer -dates
- openssl x509 -in cert.pem -text -noout | head -40
- openssl verify -CAfile ca-bundle.pem server.pem

### certificate-generation
Generate CSRs, self-signed certs, and renew with certbot.

**Commands:**
- `openssl req -new -newkey rsa:2048 -nodes -keyout key.pem -out csr.pem`
- `openssl req -x509 -newkey rsa:2048 -nodes -days 365 -keyout key.pem -out cert.pem`
- `openssl x509 -req -in csr.pem -signkey key.pem -out cert.pem -days 365`
- `certbot certonly --standalone -d localhost`
- `certbot renew --dry-run`

**Examples:**
- openssl req -new -newkey rsa:2048 -nodes -keyout key.pem -out csr.pem
- certbot certonly --standalone -d localhost
- certbot renew --dry-run

### protocol-scanning
Check TLS protocol and cipher support.

**Commands:**
- `sslscan localhost`
- `sslscan --tls-min-version 1.2 localhost`
- `openssl s_client -connect localhost:443 -tls1_2 -servername localhost`
- `nmap --script ssl-enum-ciphers -p 443 localhost`

**Examples:**
- sslscan localhost
- nmap --script ssl-enum-ciphers -p 443 localhost
- openssl s_client -connect localhost:443 -tls1_3 -servername localhost