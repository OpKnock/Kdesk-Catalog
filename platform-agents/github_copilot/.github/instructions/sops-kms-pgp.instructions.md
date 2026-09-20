---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# SOPS KMS PGP

Encrypts files with SOPS using AWS KMS keys and PGP recipients. Supports mixed recipient policies, edits encrypted files in place, patches single values, and scales to many files via .sops.yaml creation rules for team-based secret management.

## Instructions

# SOPS (KMS / PGP)

Hand-crafted skill for SOPS encryption with AWS KMS and PGP recipients.

## What this skill does

- Encrypts files with AWS KMS-managed data keys
- Encrypts with PGP fingerprints for team access
- Edits and decrypts in place, and scales via .sops.yaml creation rules

## When to use

- Teams already on AWS KMS wanting key rotation for free
- Mixing recipients: some KMS, some PGP
- Many config files with one policy, driven by creation rules

## Real commands

```bash
# Encrypt with an AWS KMS key
sops --kms arn:aws:kms:us-east-1:123456789012:key/abc --encrypt config/prod.yaml > config/prod.enc.yaml

# Encrypt with a PGP fingerprint
sops --pgp 8D7B6F2D4A1C9E3F --encrypt config/prod.yaml

# Decrypt
sops --decrypt config/prod.enc.yaml

# Edit in place (decrypt, open editor, re-encrypt)
sops --edit config/prod.enc.yaml

# Patch a single value
sops --set '["database"]["host"] "db.internal"' config/prod.enc.yaml

# Short flags with a rule set
sops -e config/staging.yaml > config/staging.enc.yaml
```

## .sops.yaml

```yaml
creation_rules:
  - path_regex: config/prod.*\.yaml
    kms: arn:aws:kms:us-east-1:123456789012:key/abc
  - path_regex: config/dev.*\.yaml
    pgp: 8D7B6F2D4A1C9E3F
```

## Testing

```bash
sops --decrypt config/prod.enc.yaml | jq '.database.host'
sops --decrypt config/prod.enc.yaml > /dev/null && echo 'decrypt ok'
```

## Best practices

- Use KMS for cloud teams, PGP for hybrid teams; rotate recipients quarterly
- Grant KMS usage (kms:Decrypt) only to deployers
- Keep .sops.yaml committed so `sops -e` needs no flags

## Capabilities

### sops-kms-pgp
Encrypts files with SOPS using AWS KMS keys and PGP recipients. Supports mixed recipient policies, edits encrypted files in place, patches single values, and scales to many files via .sops.yaml creation rules for team-based secret management.

**Commands:**
- `sops --kms arn:aws:kms:us-east-1:123456789012:key/abc --encrypt config/prod.yaml`
- `sops --pgp 8D7B6F2D4A1C9E3F --encrypt config/prod.yaml`
- `sops --decrypt config/prod.enc.yaml`
- `sops --edit config/prod.enc.yaml`
- `sops --set '["database"]["host"] "db.internal"' config/prod.enc.yaml`
- `sops -e config/staging.yaml`

**Examples:**
- sops --kms arn:aws:kms:us-east-1:123456789012:key/abc --encrypt config/prod.yaml
- sops --pgp 8D7B6F2D4A1C9E3F --encrypt config/prod.yaml
- sops --decrypt config/prod.enc.yaml
- sops --edit config/prod.enc.yaml
- sops --set '["database"]["host"] "db.internal"' config/prod.enc.yaml
