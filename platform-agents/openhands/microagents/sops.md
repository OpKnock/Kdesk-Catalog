---
name: "sops"
description: "Encrypts YAML/JSON/ENV files with SOPS keys (age, KMS, PGP): edit, set values, decrypt, and GitOps integration."
type: knowledge
triggers: ["sops", "encrypt-decrypt", "edit-and-manage"]
---

# Sops

Encrypts YAML/JSON/ENV files with SOPS keys (age, KMS, PGP): edit, set values, decrypt, and GitOps integration.

## Instructions

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
