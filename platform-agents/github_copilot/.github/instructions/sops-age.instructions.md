---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# SOPS Age

Encrypts configuration files with SOPS using age encryption keys. Generates age keypairs, encrypts and decrypts YAML/JSON files, patches individual values in encrypted files without disk decryption, and manages creation rules for GitOps workflows.

## Instructions

# SOPS with age

Hand-crafted skill for encrypting config files with SOPS using age keys.

## What this skill does

- Generates age keypairs and derives the public recipient key
- Encrypts and decrypts YAML/JSON config files with sops
- Rotates keys and patches individual values in encrypted files

## When to use

- Storing env configs with secrets in a git repo
- Local-first secret management without a KMS
- Offboarding a teammate: remove their key, rotate

## Real commands

```bash
# Generate the keypair (keep age.key safe, share only the public key)
age-keygen -o age.key
age-keygen -y age.key   # prints the age1... public key

# Encrypt a config file
sops --age age1qxyzyqmvwec5xxh9rfld7f2lcgpfqyq0q8c9dk4tw3j3e2y3rms9qe5jwcq --encrypt secrets/application.yaml > secrets/application.enc.yaml

# Decrypt for local use
sops --decrypt secrets/application.enc.yaml

# Patch one value without decrypting to disk
sops --set '["db"]["password"] "newpass"' secrets/application.enc.yaml

# Re-encrypt with the current key set
sops --rotate-keys secrets/application.enc.yaml
```

## .sops.yaml creation rules

```yaml
creation_rules:
  - path_regex: secrets/.*\.yaml
    age: age1qxyzyqmvwec5xxh9rfld7f2lcgpfqyq0q8c9dk4tw3j3e2y3rms9qe5jwcq
```

With creation rules in place: `sops --encrypt secrets/application.yaml` needs no key flag.

## Testing

```bash
sops --decrypt secrets/application.enc.yaml | yq '.db.password'
sops --encrypt secrets/application.yaml   # rule-based, no flags
```

## Best practices

- Encrypt whole files, never a single value, so the format stays honest
- Keep age.key out of the repo and backups: recovery depends on it
- Remove a leaver's key and run sops --rotate-keys immediately

## Capabilities

### sops-age
Encrypts configuration files with SOPS using age encryption keys. Generates age keypairs, encrypts and decrypts YAML/JSON files, patches individual values in encrypted files without disk decryption, and manages creation rules for GitOps workflows.

**Commands:**
- `age-keygen -o age.key`
- `age-keygen -y age.key`
- `sops --age age1qxyzyqmvwec5xxh9rfld7f2lcgpfqyq0q8c9dk4tw3j3e2y3rms9qe5jwcq --encrypt secrets/application.yaml`
- `sops --decrypt secrets/application.enc.yaml`
- `sops --set '["db"]["password"] "newpass"' secrets/application.enc.yaml`
- `sops --rotate-keys secrets/application.enc.yaml`

**Examples:**
- age-keygen -o age.key
- sops --age age1qxyzyqmvwec5xxh9rfld7f2lcgpfqyq0q8c9dk4tw3j3e2y3rms9qe5jwcq --encrypt secrets/application.yaml
- sops --decrypt secrets/application.enc.yaml
- sops --set '["db"]["password"] "newpass"' secrets/application.enc.yaml
- sops --rotate-keys secrets/application.enc.yaml
