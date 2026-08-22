---
type: agent_requested
description: "Installs and switches Node.js versions with nvm: version management, aliases, .nvmrc files, and per-project Node selection."
---

# Nvm

Installs and switches Node.js versions with nvm: version management, aliases, .nvmrc files, and per-project Node selection.

## Instructions

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