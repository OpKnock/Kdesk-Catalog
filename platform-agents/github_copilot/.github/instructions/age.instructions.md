---
applyTo: "**/*.r **/*.sh"
---

Encrypts and decrypts files with age: key generation, recipient-based encryption, passphrase files, piping, and SSH-key conversion.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `age-keygen -o key.txt`, `age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn`
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

**Parameters:**
- `output` (string): Path to write the generated key file
- `identity` (string): Private key file to derive the public key from

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

**Parameters:**
- `recipient` (string): age1... recipient public key or --recipients-file
- `identity` (string): Key file to decrypt with (-d -i)
- `passphrase` (boolean): -p uses an interactive passphrase instead of keys

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

## References
- [age Specification](https://age-encryption.org/v1)
- [age GitHub](https://github.com/FiloSottile/age)
- [ssh-to-age](https://github.com/FiloSottile/age/tree/main/ssh-to-age)
