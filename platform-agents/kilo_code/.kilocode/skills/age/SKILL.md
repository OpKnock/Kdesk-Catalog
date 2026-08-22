---
name: "age"
description: "Encrypts and decrypts files with age: key generation, recipient-based encryption, passphrase files, piping, and SSH-key conversion."
---

# Age

Encrypts and decrypts files with age: key generation, recipient-based encryption, passphrase files, piping, and SSH-key conversion.

## Instructions

# age

## What this skill does

Encrypts and decrypts files with age: key generation, recipient-based encryption, passphrase mode, streaming/pipe usage, and converting SSH keys into age identities.

## When to use

- Sealing env files, kubeconfigs, or backups before storing them
- Sharing encrypted files with a team without a KMS
- Reusing existing SSH keys for encryption

## Real commands

```bash
# Generate a keypair
age-keygen -o key.txt
chmod 600 key.txt

# Encrypt to a recipient
age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p -o secret.age secret.txt

# Decrypt with the identity file
age -d -i key.txt -o secret.txt secret.age

# Passphrase-protected file
age -p -o secret.age secret.txt

# Pipe archives through age
tar czf - ./data | age -r $(cat recipient.txt) > data.tar.gz.age
```

## SSH key conversion

```bash
ssh-to-age -private-key -i ~/.ssh/id_ed25519 > key.txt
age-keygen -y -i key.txt   # derive the recipient
```

## Testing

- Round-trip: encrypt then decrypt and compare with sha256sum
- Test recipient mode with a freshly generated keypair

## Best practices

- Always chmod 600 key files
- Prefer recipient files over pasting long keys in shell history
- Store recipient (public) keys in the repo, identity files outside

## Capabilities

### key-management
Generate age keypairs, derive public keys, and convert SSH keys.

**Commands:**
- `age-keygen -o key.txt`
- `age-keygen -y -i key.txt`
- `chmod 600 key.txt`
- `ssh-to-age -private-key -i ~/.ssh/id_ed25519 > key.txt`
- `age-keygen -o ~/.config/age/keys.txt`

**Examples:**
- age-keygen -y -i key.txt | tee recipient.txt
- ssh-to-age -private-key -i ~/.ssh/id_ed25519 > age-key.txt
- age-keygen -o key.txt && chmod 600 key.txt

### encrypt-decrypt
Encrypt and decrypt files and streams with recipients or passphrases.

**Commands:**
- `age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p -o secret.age secret.txt`
- `age -d -i key.txt -o secret.txt secret.age`
- `age -p -o secret.age secret.txt`
- `age -d secret.age`
- `tar czf - ./data | age -r $(cat recipient.txt) > data.tar.gz.age`

**Examples:**
- age -r age1... -o secret.age secret.txt
- age -d -i key.txt secret.age
- age -p -o kubeconfig.age kubeconfig
