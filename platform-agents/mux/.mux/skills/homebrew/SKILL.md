---
name: "homebrew"
description: "Installs and manages macOS/Linux software with Homebrew: formulae, casks, services, cleanup, and Brewfile workflows."
---

# Homebrew

Installs and manages macOS/Linux software with Homebrew: formulae, casks, services, cleanup, and Brewfile workflows.

## Instructions

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
