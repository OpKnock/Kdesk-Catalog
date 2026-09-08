---
name: "Gpg"
description: "PGP encryption and signing: generate keypairs, encrypt/decrypt files, sign and verify commits, and manage keyrings. Use when working with gpg ops, api or when the user mentions gpg ops, api."
globs: ["**/*.r", "**/*.rs", "**/*.sh"]
alwaysApply: false
---

PGP encryption and signing: generate keypairs, encrypt/decrypt files, sign and verify commits, and manage keyrings.

## Agentic Workflow: Read -> Reason -> Act (gpg)

You are **Gpg** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gpg`
- Domain: PGP encryption and signing: generate keypairs, encrypt/decrypt files, sign and verify commits, and manage keyrings.
- **gpg-ops**: Generate keys, encrypt/decrypt, sign/verify, and manage keyring exports. — `gpg --full-generate-key`
- Check `knowledge` and `prerequisites: gpg`

### 2. Reason — think for `gpg`
- For `gpg-ops`: Generate keys, encrypt/decrypt, sign/verify, and manage keyring exports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gpg` tools
- Tools: `Glob`, `Grep`, `Read`, `Gpg` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gpg:85718c9b`

# GPG

## What this skill does

GPG (GnuPG) implements OpenPGP: asymmetric encryption, digital signatures, and key management. It protects files at rest and proves authorship of commits and releases.

## When to use

- Encrypting files exchanged with partners
- Signing commits/tags for supply chain trust
- Managing keyrings for CI release signing

## Real commands

```bash
# Generate a keypair
gpg --full-generate-key

# Encrypt/decrypt
gpg --encrypt --recipient alice@example.com secrets.txt
gpg --decrypt secrets.txt.gpg

# Sign and verify
gpg --sign --local-user bob@example.com data.txt
gpg --verify data.txt.gpg

# Export/import public keys
gpg --armor --export alice@example.com > alice.pub
gpg --import alice.pub

# Keyring
 gpg --list-keys --fingerprint
```

## Signing commits

```bash
git config --global user.signingkey <fingerprint>
git config --global commit.gpgsign true
git commit -S -m "signed commit"
```

## Key backup

```bash
# Export the secret key (keep offline!) and revoke cert
gpg --armor --export-secret-keys alice@example.com > alice-secret.asc
gpg --gen-revoke alice@example.com > alice-revoke.asc
```

## Testing

```bash
# Round trip
echo topsecret | gpg --encrypt --recipient alice@example.com | gpg --decrypt
```

## Best practices

- Use 4096-bit RSA or modern ECC keys; avoid legacy defaults.
- Back up secret keys and revocation certs offline.
- Sign, then encrypt (sign-then-encrypt) rather than the reverse.
- Keep a separate signing subkey for CI agents.
- Never share secret keys; share only armored public keys.

## Capabilities

### gpg-ops
Generate keys, encrypt/decrypt, sign/verify, and manage keyring exports.

**Parameters:**
- `recipient` (string): Key id or email of the recipient
- `input-file` (string): File to encrypt/sign/decrypt
- `key-id` (string): Local key id or fingerprint

**Commands:**
- `gpg --full-generate-key`
- `gpg --encrypt --recipient alice@localhost secrets.txt`
- `gpg --decrypt secrets.txt.gpg`
- `gpg --sign --local-user bob@localhost data.txt`
- `gpg --verify data.txt.gpg`
- `gpg --armor --export alice@localhost > alice.pub`
- `gpg --list-keys`

**Examples:**
- gpg --encrypt --recipient alice@localhost secrets.txt && gpg --decrypt secrets.txt.gpg
- gpg --armor --export alice@localhost > alice.pub && gpg --import alice.pub
- gpg --list-keys --fingerprint

## References
- [GnuPG documentation](https://www.gnupg.org/documentation/manuals/gnupg/)
- [GPG CLI cheat sheet](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)