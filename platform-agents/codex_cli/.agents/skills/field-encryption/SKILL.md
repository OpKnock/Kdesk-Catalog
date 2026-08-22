---
name: "field-encryption"
description: "Column-level and field-level encryption: encrypt sensitive database fields with pgcrypto, envelope encryption in app code, and searchability trade-offs."
---

# Field Encryption

Column-level and field-level encryption: encrypt sensitive database fields with pgcrypto, envelope encryption in app code, and searchability trade-offs.

## Instructions

# Field Encryption

## What this skill does

Field encryption protects individual columns or object fields (emails, SSNs, payment tokens) rather than the whole disk. pgcrypto encrypts inside PostgreSQL; app-level envelope encryption uses KMS data keys.

## When to use

- Compliance requirements targeting specific data elements
- Protecting PII in databases that can't be fully encrypted
- Limiting blast radius if a backup leaks

## Real commands

```bash
# pgcrypto in PostgreSQL
psql -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
psql -c "SELECT pgp_sym_encrypt('sensitive value', 'secret-passphrase') AS cipher;"
psql -c "SELECT pgp_sym_decrypt(pgp_sym_encrypt('value','pass'), 'pass');"

# KMS data key for envelope encryption
aws kms generate-data-key --key-id alias/my-key --key-spec AES_256 --output json | jq -r '.CiphertextBlob'
aws kms decrypt --ciphertext-blob fileb://envelope.blob --output json | jq -r '.Plaintext'
```

## Schema example

```sql
ALTER TABLE users ADD COLUMN email_cipher bytea;
UPDATE users SET email_cipher = pgp_sym_encrypt(email, 'app-key');
ALTER TABLE users DROP COLUMN email;
```

## Envelope encryption pattern

1. `generate-data-key` in KMS: returns plaintext key + encrypted key blob.
2. Encrypt the field with the plaintext data key (AES-256-GCM) in the app.
3. Store ciphertext + encrypted key blob; discard the plaintext key.
4. To decrypt: `kms decrypt` the blob, decrypt the field.

## Testing

```bash
# Round trip must be lossless
psql -t -c "SELECT pgp_sym_decrypt(pgp_sym_encrypt('roundtrip','k'), 'k') = 'roundtrip';"
```

## Best practices

- Encrypt at rest AND at the field level for highest-risk attributes only; every field has a cost.
- Keep keys out of the DB; use KMS or a vault, with rotation.
- Be aware you lose equality lookups: precompute a hash column for exact match.
- Log decryption access (e.g. pgaudit or app audit) for sensitive fields.
- Test key rotation end to end before rolling out.

## Capabilities

### column-encryption
Encrypt and decrypt specific fields with pgcrypto and application-level envelope keys.

**Commands:**
- `psql -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"`
- `psql -c "SELECT pgp_sym_encrypt('sensitive value', 'secret-passphrase') AS cipher;"`
- `psql -c "SELECT pgp_sym_decrypt(pgp_sym_encrypt('value','pass'), 'pass');"`
- `aws kms generate-data-key --key-id alias/my-key --key-spec AES_256 --output json | jq -r '.CiphertextBlob'`
- `psql -c "SELECT id, pgp_sym_decrypt(email_cipher, 'app-key') FROM users WHERE id = 1;"`

**Examples:**
- psql -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
- aws kms generate-data-key --key-id alias/my-key --key-spec AES_256 --output json | jq -r '.CiphertextBlob'
- psql -c "SELECT id, pgp_sym_decrypt(email_cipher, 'app-key') FROM users WHERE id = 1;"
