---
name: "encryption-at-rest"
description: "Data-at-rest encryption: full-disk encryption with LUKS, file encryption with openssl, and key management with cloud KMS services."
type: knowledge
triggers: ["encryption-at-rest", "disk-encryption"]
---

# Encryption At Rest

Data-at-rest encryption: full-disk encryption with LUKS, file encryption with openssl, and key management with cloud KMS services.

## Instructions

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
