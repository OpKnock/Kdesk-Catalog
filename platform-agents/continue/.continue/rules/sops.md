---
name: "Sops"
description: "Encrypts YAML/JSON/ENV files with SOPS keys (age, KMS, PGP): edit, set values, decrypt, and GitOps integration. Use when working with encrypt decrypt, edit and manage, devops or when the user mentions encrypt decrypt, edit and manage, devops."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Encrypts YAML/JSON/ENV files with SOPS keys (age, KMS, PGP): edit, set values, decrypt, and GitOps integration.

## Agentic Workflow: Read -> Reason -> Act (sops)

You are **Sops** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `sops`
- Domain: Encrypts YAML/JSON/ENV files with SOPS keys (age, KMS, PGP): edit, set values, decrypt, and GitOps integration.
- **encrypt-decrypt**: Encrypt and decrypt files with configured key services. — `sops -e -i secrets.yaml`
- **edit-and-manage**: Edit encrypted values in place and manage key services. — `sops secrets.yaml`
- Check `knowledge` and `prerequisites: sops`

### 2. Reason — think for `sops`
- For `encrypt-decrypt`: Encrypt and decrypt files with configured key services. — decide which checks to run
- For `edit-and-manage`: Edit encrypted values in place and manage key services. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sops` tools
- Tools: `Glob`, `Grep`, `Read`, `Sops` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sops:43c0193f`

# SOPS Secret Encryption

Keep secrets encrypted in git with SOPS while keeping them usable in CI and clusters.

## What This Skill Does

- Encrypts/decrypts YAML, JSON, ENV, and INI files
- Works with age, AWS/GCP/Azure KMS, and PGP keys
- Edits encrypted files safely (sops opens the editor with decryption)
- Sets individual values without exposing the rest
- Integrates with Flux/Kustomize decryption providers

## When to Use

- Secrets in GitOps repositories
- Encrypted env files for CI
- Preferring file-level encryption over cluster-only encryption

## Real Commands

```bash
# Encrypt / decrypt
sops -e -i secrets.yaml
sops -d secrets.yaml
sops --encrypt --age age1xyz... secrets.env > secrets.enc.env
sops --decrypt secrets.yaml | kubectl apply -f -

# Edit in place
sops secrets.yaml                          # opens editor, saves encrypted
sops --set '["db"]["password"] "newpass"' secrets.yaml
sops --set --encrypt '["db"]["password"] "raw-new-pass"' secrets.yaml

# Convert and manage
sops --input-type yaml --output-type json -e config.yaml > config.json
sops --decrypt --output decrypted.yaml secrets.yaml
sops updatekeys --yes secrets.yaml          # re-encrypt for new keys
sops --verbose -e secrets.yaml
```

## .sops.yaml Example

```yaml
creation_rules:
  - path_regex: \.secrets\.yaml$
    age: age1xyz...
  - path_regex: \.env$
    kms: arn:aws:kms:us-east-1:123456789012:key/abc
```

## Best Practices

- Set creation_rules per path and key service
- Keep recipient keys (public) in the repo; private keys in CI secrets
- Decrypt to stdout, never write plaintext copies to disk
- Use sops exec-env to load decrypted envs into processes
- Rotate keys by running updatekeys after key changes

## Capabilities

### encrypt-decrypt
Encrypt and decrypt files with configured key services.

**Parameters:**
- `file` (string): File to encrypt/decrypt
- `key` (string): age or key-service identifier

**Commands:**
- `sops -e -i secrets.yaml`
- `sops -d secrets.yaml`
- `sops --encrypt --age age1xyz... secrets.env`
- `sops --decrypt secrets.yaml | kubectl apply -f -`
- `sops --input-type yaml --output-type json -e config.yaml > config.json`

**Examples:**
- sops -e -i secrets.yaml
- sops --decrypt secrets.yaml | kubectl apply -f -
- sops --encrypt --age age1xyz... secrets.env

### edit-and-manage
Edit encrypted values in place and manage key services.

**Parameters:**
- `path` (string): JSON path to value, e.g. ["db"]["password"]
- `value` (string): New value

**Commands:**
- `sops secrets.yaml`
- `sops --set '["db"]["password"] "newpass"' secrets.yaml`
- `sops --set --encrypt '["db"]["password"] "raw-new"' secrets.yaml`
- `sops --decrypt --output decrypted.yaml secrets.yaml`
- `sops updatekeys --yes secrets.yaml`
- `sops --verbose -e secrets.yaml`

**Examples:**
- sops secrets.yaml
- sops --set '["db"]["password"] "newpass"' secrets.yaml
- sops updatekeys --yes secrets.yaml

## References
- [SOPS (getsops)](https://github.com/getsops/sops)
- [SOPS for GitOps](https://fluxcd.io/flux/guides/mozilla-sops/)