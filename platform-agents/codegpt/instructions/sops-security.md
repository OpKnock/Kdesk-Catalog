# sops-security

Encrypts YAML/JSON/ENV files with age, PGP, KMS, or Vault keys using SOPS, with git integration for secrets management.

## Instructions

# SOPS

Secrets as encrypted files: edit, commit, decrypt at deploy time.

## What This Skill Does

- Encrypts YAML, JSON, ENV, and binary files with per-value encryption
- Uses age, PGP, KMS, or Vault key providers
- Edits encrypted files in place without exposing values
- Integrates with git diff for reviewable secret changes

## When to Use

- Secrets in GitOps repos with KMS-backed decryption
- Team workflows that review secret changes in PRs
- Replacing plaintext config files in CI

## Real Commands

```bash
# Encrypt with age
sops -e --age age1q... secrets.yaml > secrets.enc.yaml

# Encrypt in place
sops -e -i secrets.yaml

# Decrypt
sops -d secrets.enc.yaml

# Edit interactively (decrypts in memory)
sops secrets.enc.yaml

# Set values non-interactively
sops --set '["db_password"] "newpass"' secrets.enc.yaml

# KMS-backed
sops -e --kms arn:aws:kms:us-east-1:123456789012:key/abcd secrets.yaml

# Update keys after rotation
sops updatekeys secrets.enc.yaml
```

## .sops.yaml

```yaml
creation_rules:
  - path_regex: secrets/.*\.yaml
    age: age1q...
  - path_regex: prod/.*\.env
    kms: arn:aws:kms:us-east-1:123456789012:key/abcd
```

## Best Practices

- Define creation_rules so sops picks keys by path automatically
- Never commit plaintext versions of encrypted files
- Rotate keys and run sops updatekeys on all files
- Use KMS/age keys over PGP where possible for automation
- Configure the git diff textconv so PRs show readable diffs

## Capabilities

### file-encryption
Encrypt and decrypt config files with key providers.

**Commands:**
- `sops -e secrets.yaml > secrets.enc.yaml`
- `sops -d secrets.enc.yaml`
- `sops -e --age age1q... secrets.yaml`
- `sops -e --pgp ABCDEF... secrets.yaml`
- `sops -e -i secrets.yaml`

**Examples:**
- sops -e secrets.yaml > secrets.enc.yaml
- sops -d secrets.enc.yaml
- sops -e -i secrets.yaml

### editing-and-kms
Edit encrypted values and use cloud KMS keys.

**Commands:**
- `sops secrets.enc.yaml`
- `sops --set '["db_password"] "newpass"' secrets.enc.yaml`
- `sops --set '["db"]["host"] "db.internal"' secrets.enc.yaml`
- `sops -e --kms arn:aws:kms:us-east-1:123456789012:key/abcd secrets.yaml`
- `sops -k -e secrets.yaml`

**Examples:**
- sops secrets.enc.yaml
- sops --set '["api_key"] "xyz"' secrets.enc.yaml
- sops -e --kms arn:aws:kms:... secrets.yaml

### git-integration
Use sops with git diff and merge tools.

**Commands:**
- `git config --global diff.sopsdiffer.textconv "sops -d"`
- `git config --global merge.sopsmerge.driver "sops merge-file --output %A %O %A %B"`
- `sops updatekeys secrets.enc.yaml`
- `sops --config .sops.yaml -e secrets.yaml`

**Examples:**
- git config --global diff.sopsdiffer.textconv "sops -d"
- sops updatekeys secrets.enc.yaml
- sops --config .sops.yaml -e secrets.yaml
