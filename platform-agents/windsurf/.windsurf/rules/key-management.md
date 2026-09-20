---
trigger: glob
description: "Manage cryptographic keys across local openssl and cloud KMS (AWS KMS, GCP KMS, HashiCorp Vault): generation, encryption, and secure storage."
globs: ["**/*.r", "**/*.sh"]
---

# Key Management

Manage cryptographic keys across local openssl and cloud KMS (AWS KMS, GCP KMS, HashiCorp Vault): generation, encryption, and secure storage.

## Instructions

# Key Management

Generate, encrypt, and store keys and secrets across local and cloud tooling.

## What this skill does

- Creates RSA/EC key pairs and self-signed certs with openssl.
- Encrypts/decrypts with AWS KMS and GCP Cloud KMS.
- Stores secrets in HashiCorp Vault.

## When to use

- Bootstrapping TLS for internal services.
- Envelope-encrypting secrets before they hit disk or CI logs.
- Centralizing secrets with versioning and audit (Vault/KMS).

## Real commands

```bash
# Local RSA keypair
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

# EC key for ECDSA JWT signing
openssl ecparam -name prime256v1 -genkey -noout -out ec-key.pem

# Self-signed cert
openssl req -x509 -new -key private.pem -days 365 -out cert.pem \
  -subj '/CN=api.staging.myapp.test'

# AWS KMS encrypt/decrypt
aws kms encrypt --key-id alias/orders-key \
  --plaintext fileb://secret.txt --output text --query CiphertextBlob > secret.b64
aws kms decrypt --ciphertext-blob fileb://secret.bin \
  --query Plaintext --output text | base64 -d > secret.txt

# GCP KMS encrypt/decrypt
gcloud kms encrypt --location=global --keyring=my-ring --key=my-key \
  --plaintext-file=secret.txt --ciphertext-file=secret.enc
gcloud kms decrypt --location=global --keyring=my-ring --key=my-key \
  --ciphertext-file=secret.enc --plaintext-file=out.txt

# Vault KV
vault kv put secret/api api_key=supersecret
vault kv get secret/api
```

## Testing

```bash
# Round-trip test: decrypt equals the original
cmp secret.txt out.txt && echo OK
```

## Best practices

- Keep private keys out of repos; use KMS/Vault for production secrets.
- Use KMS envelope encryption: encrypt data keys, not data blobs.
- Rotate keys on a schedule and disable old versions in KMS.

## Capabilities

### openssl-keys
Generate RSA/EC key pairs and certificates locally.

**Commands:**
- `openssl genrsa -out private.pem 2048`
- `openssl rsa -in private.pem -pubout -out public.pem`
- `openssl ecparam -name prime256v1 -genkey -noout -out ec-key.pem`
- `openssl req -x509 -new -key private.pem -days 365 -out cert.pem -subj '/CN=api.staging.myapp.test'`

**Examples:**
- openssl genrsa -out private.pem 2048
- openssl ecparam -name prime256v1 -genkey -noout -out ec-key.pem
- openssl req -x509 -new -key private.pem -days 365 -out cert.pem -subj '/CN=api.staging.myapp.test'

### cloud-kms
Encrypt and decrypt data with AWS KMS, GCP KMS, and Vault.

**Commands:**
- `aws kms encrypt --key-id alias/orders-key --plaintext fileb://secret.txt --output text --query CiphertextBlob > secret.b64`
- `aws kms decrypt --ciphertext-blob fileb://secret.bin --query Plaintext --output text | base64 -d > secret.txt`
- `gcloud kms encrypt --location=global --keyring=my-ring --key=my-key --plaintext-file=secret.txt --ciphertext-file=secret.enc`
- `gcloud kms decrypt --location=global --keyring=my-ring --key=my-key --ciphertext-file=secret.enc --plaintext-file=out.txt`
- `vault kv put secret/api api_key=supersecret`

**Examples:**
- aws kms encrypt --key-id alias/orders-key --plaintext fileb://secret.txt --output text --query CiphertextBlob > secret.b64
- gcloud kms encrypt --location=global --keyring=my-ring --key=my-key --plaintext-file=secret.txt --ciphertext-file=secret.enc
- vault kv get secret/api
