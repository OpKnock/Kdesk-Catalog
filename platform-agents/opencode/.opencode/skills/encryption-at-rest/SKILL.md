---
name: "encryption-at-rest"
description: "Data-at-rest encryption: full-disk encryption with LUKS, file encryption with openssl, and key management with cloud KMS services. Use when working with disk encryption, api or when the user mentions disk encryption, api."
---

Data-at-rest encryption: full-disk encryption with LUKS, file encryption with openssl, and key management with cloud KMS services.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `sudo cryptsetup luksFormat /dev/sdb1`
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

# Encryption at Rest

## What this skill does

Encryption at rest protects data written to disk. LUKS encrypts whole block devices; openssl enc handles individual files; KMS provides managed keys for envelope encryption in cloud applications.

## When to use

- Encrypting a new data disk or VM image
- Storing secrets in files that must survive on disk
- Adding envelope encryption to database backups

## Real commands

```bash
# LUKS full-disk encryption
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup open /dev/sdb1 secretdata
sudo mkfs.ext4 /dev/mapper/secretdata
sudo mount /dev/mapper/secretdata /mnt/secure

# File encryption with password-derived key
openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -in secrets.txt -out secrets.txt.enc
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in secrets.txt.enc -out secrets.txt

# Envelope encryption with KMS
aws kms encrypt --key-id alias/my-key --plaintext fileb://payload.bin --output text --query CiphertextBlob | base64 -d > payload.enc
aws kms decrypt --ciphertext-blob fileb://payload.enc --output text --query Plaintext | base64 -d
```

## Auto-mount with keyfile

```bash
sudo dd if=/dev/urandom of=/etc/luks/keyfile bs=64 count=1
sudo cryptsetup luksAddKey /dev/sdb1 /etc/luks/keyfile
# /etc/crypttab: secretdata UUID=<luks-uuid> /etc/luks/keyfile luks
```

## Testing

```bash
# Verify the volume is encrypted
sudo cryptsetup luksDump /dev/sdb1 | head -12
sudo lsblk -o NAME,TYPE,MOUNTPOINT /dev/sdb1
```

## Best practices

- Always back up the LUKS header: `cryptsetup luksHeaderBackup /dev/sdb1 --header-backup-file header.bak`.
- Use `-pbkdf2 -iter 200000` (or Argon2) rather than legacy key derivation.
- Store KMS keys in a separate account or environment from the data.
- Rotate file keys periodically and re-encrypt backups.

## Capabilities

### disk-encryption
Set up LUKS volumes, encrypt files with openssl, and manage keys via AWS KMS.

**Parameters:**
- `device` (string): Block device to encrypt, e.g. /dev/sdb1
- `cipher` (string): Cipher for openssl enc, e.g. aes-256-cbc
- `kms-key-id` (string): KMS key id or alias for envelope encryption

**Commands:**
- `sudo cryptsetup luksFormat /dev/sdb1`
- `sudo cryptsetup open /dev/sdb1 secretdata && sudo mkfs.ext4 /dev/mapper/secretdata`
- `openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -in secrets.txt -out secrets.txt.enc`
- `openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in secrets.txt.enc -out secrets.txt`
- `aws kms encrypt --key-id alias/my-key --plaintext fileb://payload.bin --output text --query CiphertextBlob | base64 -d > payload.enc`

**Examples:**
- sudo cryptsetup luksFormat /dev/sdb1 && sudo cryptsetup open /dev/sdb1 secretdata
- openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -in secrets.txt -out secrets.txt.enc
- aws kms decrypt --ciphertext-blob fileb://payload.enc --output text --query Plaintext | base64 -d

## References
- [cryptsetup/LUKS](https://gitlab.com/cryptsetup/cryptsetup/-/wikis/home)
- [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
