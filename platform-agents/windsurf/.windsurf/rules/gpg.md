---
trigger: glob
description: "PGP encryption and signing: generate keypairs, encrypt/decrypt files, sign and verify commits, and manage keyrings."
globs: ["**/*.r", "**/*.rs", "**/*.sh"]
---

# Gpg

PGP encryption and signing: generate keypairs, encrypt/decrypt files, sign and verify commits, and manage keyrings.

## Instructions

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
