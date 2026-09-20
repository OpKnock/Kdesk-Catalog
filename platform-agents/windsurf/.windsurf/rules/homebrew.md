---
trigger: glob
description: "Installs and manages macOS/Linux software with Homebrew: formulae, casks, services, cleanup, and Brewfile workflows. Use when working with package operations, services and cleanup, devtools or when the user mentions package operations, services and cleanup, devtools."
globs: ["**/*.r", "**/*.rb", "**/*.sh", "**/*.sql"]
---

Installs and manages macOS/Linux software with Homebrew: formulae, casks, services, cleanup, and Brewfile workflows.

## Agentic Workflow: Read -> Reason -> Act (homebrew)

You are **Homebrew** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `homebrew`
- Domain: Installs and manages macOS/Linux software with Homebrew: formulae, casks, services, cleanup, and Brewfile workflows.
- **package-operations**: Install, search, upgrade, and uninstall formulae and casks. — `brew search postgres`
- **services-and-cleanup**: Run background services and maintain a clean brew state. — `brew services start postgresql@16`
- Check `knowledge` and `prerequisites: brew`

### 2. Reason — think for `homebrew`
- For `package-operations`: Install, search, upgrade, and uninstall formulae and casks. — decide which checks to run
- For `services-and-cleanup`: Run background services and maintain a clean brew state. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `homebrew` tools
- Tools: `Glob`, `Grep`, `Read`, `Brew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `homebrew:00f8e142`

# Homebrew Package Management

Install and manage open-source software on macOS/Linux with Homebrew.

## What This Skill Does

- Installs formulae (CLI tools) and casks (GUI apps)
- Searches, upgrades, and uninstalls packages
- Manages background services (brew services)
- Cleans caches and orphaned dependencies
- Creates Brewfiles for machine bootstrapping

## When to Use

- Installing dev tools on macOS
- Bootstrapping a new machine from a Brewfile
- Managing services like postgres/redis locally

## Real Commands

```bash
# Install
brew search postgres
brew install postgresql@16
brew install --cask docker
brew install --formula jq yq

# Update
brew update
brew upgrade
brew upgrade postgresql@16

# Uninstall
brew uninstall postgresql@16
brew uninstall --cask docker

# Services
brew services start postgresql@16
brew services list
brew services stop redis
brew services restart --all

# Maintenance
brew cleanup --prune=7
brew autoremove
brew doctor
brew list --cask
```

## Brewfile Example

```ruby
tap "homebrew/cask"
brew "jq"
brew "postgresql@16", link: true
cask "docker"
cask "visual-studio-code"
```

## Best Practices

- Commit a Brewfile and run `brew bundle` on new machines
- Prefer `brew services` over launchctl for background tools
- Run brew doctor after major macOS upgrades
- Use versioned formulae (postgresql@16) for project parity
- Clean up weekly: cleanup + autoremove

## Capabilities

### package-operations
Install, search, upgrade, and uninstall formulae and casks.

**Parameters:**
- `package` (string): Formula or cask name
- `cask` (boolean): Treat package as a GUI cask

**Commands:**
- `brew search postgres`
- `brew install postgresql@16`
- `brew install --cask docker`
- `brew upgrade`
- `brew uninstall --cask docker`
- `brew list`

**Examples:**
- brew install postgresql@16
- brew install --cask docker
- brew upgrade

### services-and-cleanup
Run background services and maintain a clean brew state.

**Parameters:**
- `service` (string): Service name
- `prune` (string): Cache age to prune

**Commands:**
- `brew services start postgresql@16`
- `brew services list`
- `brew services stop redis`
- `brew cleanup --prune=7`
- `brew autoremove`
- `brew doctor`

**Examples:**
- brew services start postgresql@16
- brew cleanup --prune=7
- brew doctor

## References
- [Homebrew Documentation](https://docs.brew.sh/)
- [Homebrew Formulae Search](https://formulae.brew.sh/)
