---
applyTo: "**/*.r **/*.sh"
---

Installs and switches Node.js versions with nvm: version management, aliases, .nvmrc files, and per-project Node selection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nvm install 20`, `nvm alias default 20`
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

# nvm Node Version Management

Run multiple Node.js versions side by side.

## What This Skill Does

- Installs Node versions (LTS, latest, exact)
- Switches versions per shell/project
- Sets default and named aliases
- Uses .nvmrc for repo-pinned versions
- Runs commands with a specific version (nvm exec)

## When to Use

- Projects pinned to different Node majors
- Testing against multiple Node versions
- Avoiding global sudo installs

## Real Commands

```bash
# Install and switch
nvm install 20
nvm install --lts
nvm use 18.20.4
nvm current
nvm ls
nvm ls-remote

# Aliases and defaults
nvm alias default 20
nvm alias project-node 18.20.4
nvm unalias project-node

# Repo-pinned version (.nvmrc = "20")
nvm use                      # reads .nvmrc
nvm install                  # installs .nvmrc version

# One-off
nvm exec 18 node -v
nvm run 18 --version

# Cleanup
nvm uninstall 16
```

## Best Practices

- Commit `.nvmrc` with major.minor.patch to pin runtime
- Add `nvm use` to your shell hook (nvm alias default + cd hook)
- Use CI matrix to test against multiple LTS versions
- Never sudo install Node globally; nvm keeps it in $HOME
- Set default to an active LTS for new projects

## Capabilities

### version-management
Install, list, and switch Node.js versions.

**Parameters:**
- `version` (string): Node version or alias, e.g. 20, --lts
- `alias` (string): Alias name

**Commands:**
- `nvm install 20`
- `nvm install --lts`
- `nvm ls`
- `nvm ls-remote`
- `nvm use 18.20.4`
- `nvm current`

**Examples:**
- nvm install 20
- nvm use 18.20.4
- nvm ls-remote --lts

### aliases-and-autoload
Set default versions, create aliases, and use .nvmrc.

**Parameters:**
- `name` (string): Alias or default name
- `version` (string): Version the alias points to

**Commands:**
- `nvm alias default 20`
- `nvm alias project-node 18.20.4`
- `nvm unalias project-node`
- `nvm use 20 >/dev/null 2>&1 || nvm install 20`
- `nvm exec 18 node -v`
- `nvm uninstall 16`

**Examples:**
- nvm alias default 20
- nvm exec 18 node -v
- nvm use 20 || nvm install 20

## References
- [nvm-sh GitHub](https://github.com/nvm-sh/nvm)
- [Node.js Releases](https://nodejs.org/en/about/previous-releases)
