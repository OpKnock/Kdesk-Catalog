Manages secrets with the 1Password CLI (op): sign-in, item CRUD, op:// references, secret injection, and running processes with loaded secrets.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `op signin --account my.1password.com`, `op read op://vault/MyLogin/password`
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

# 1Password

## What this skill does

Manages credentials with the 1Password CLI (op): sign-in flows, item CRUD, reading secrets by op:// reference, injecting secrets into templates or process environments, and shell plugins for third-party CLIs.

## When to use

- Fetching a stored password or API key for a script or deploy
- Creating vault items during automation
- Injecting secrets into .env files or process environments without echoing them

## Real commands

```bash
# Authenticate the CLI
op signin --account my.1password.com

# Create a login item
op item create --category=login --title=prod-db username=admin password=secret --vault=Infra

# Read a single field by reference
op read op://Infra/prod-db/password

# Inject into a template file
op inject -i template.env -o .env

# Run a process with secrets loaded, never printed
op run -- ./deploy.sh
```

## Template example

```env
DB_URL=op://Infra/prod-db/url
API_KEY=op://Infra/stripe/live-key
```

## Testing

- Verify items with `op item get <title> --fields username` after creation
- Test injection by running the target script with `op run` and checking it authenticates

## Best practices

- Never pipe `op read` output into logs; use `op run` when secrets must reach a subprocess
- Scope with `--account` and `--vault` in scripts to avoid ambiguity
- Use `--reveal` only on demand; output masks hidden fields by default
- Grant access via vault permissions, not shared passwords

## Capabilities

### secret-management
Create, read, and update 1Password items programmatically.

**Parameters:**
- `vault` (string): Vault to search or write into
- `fields` (string): Comma-separated field names to return
- `reveal` (boolean): Print hidden fields in plaintext

**Commands:**
- `op signin --account my.1password.com`
- `op item create --category=login --title=MyLogin username=me password=secret`
- `op item get MyLogin --fields username,password`
- `op item edit MyLogin --vault=Personal`
- `op item delete MyLogin --archive`

**Examples:**
- op item get MyLogin --fields password --reveal
- op item create --category=login --title=prod-db --url db.internal username=admin password=$(openssl rand -base64 24)
- op item list --vault=Infra --format=json

### secret-injection
Reference secrets by URI and inject into files or process environments without printing them.

**Parameters:**
- `input` (string): Template file containing op:// references
- `output` (string): Destination file for injected output
- `account` (string): 1Password account shorthand, e.g. my.1password.com

**Commands:**
- `op read op://vault/MyLogin/password`
- `op inject -i template.env -o .env`
- `op run --no-masking -- env`
- `op run -- ./deploy.sh`
- `op vault list`

**Examples:**
- op read op://Prod/db-credentials/password
- op inject -i deploy.tpl -o deploy.env
- op run -- npm run start:prod

## References
- [1Password CLI Reference](https://developer.1password.com/docs/cli/reference)
- [Secret References](https://developer.1password.com/docs/cli/secret-references)
- [Shell Plugins](https://developer.1password.com/docs/cli/shell-plugins)