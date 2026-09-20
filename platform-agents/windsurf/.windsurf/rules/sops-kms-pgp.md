---
trigger: glob
description: "Encrypts files with SOPS using AWS KMS keys and PGP recipients. Supports mixed recipient policies, edits encrypted files in place, patches single values, and scales to many files via .sops.yaml creation rules for team-based secret management. Use when working with sops kms pgp, api or when the user mentions sops kms pgp, api."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Encrypts files with SOPS using AWS KMS keys and PGP recipients. Supports mixed recipient policies, edits encrypted files in place, patches single values, and scales to many files via .sops.yaml creation rules for team-based secret management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `sops --kms arn:aws:kms:us-east-1:123456789012:key/abc --encr`
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

**Parameters:**
- `kms_arn` (string): AWS KMS key ARN for encryption
- `pgp_fingerprint` (string): PGP key fingerprint for recipient
- `file_path` (string): Path to file to encrypt/decrypt

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

## References
- [SOPS documentation](https://getsops.io/docs/)
