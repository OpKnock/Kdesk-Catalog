---
name: "sops-age"
description: "Encrypts configuration files with SOPS using age encryption keys. Generates age keypairs, encrypts and decrypts YAML/JSON files, patches individual values in encrypted files without disk decryption, and manages creation rules for GitOps workflows. Use when working with sops age, api or when the user mentions sops age, api."
---

Encrypts configuration files with SOPS using age encryption keys. Generates age keypairs, encrypts and decrypts YAML/JSON files, patches individual values in encrypted files without disk decryption, and manages creation rules for GitOps workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `age-keygen -o age.key`
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

**Parameters:**
- `age_pubkey` (string): Age public key (age1...)
- `file_path` (string): Path to YAML/JSON file to encrypt
- `key_path` (string): Path to age private key file

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

## References
- [SOPS usage docs](https://getsops.io/docs/)
