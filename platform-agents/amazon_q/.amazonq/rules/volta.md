# Volta

Manages Node.js toolchains with Volta: install and pin node/npm/yarn per project, automatic version switching, and speed.

## Instructions

# Volta Node Toolchain

Pin Node.js and package manager versions per project, switched automatically.

## What This Skill Does

- Installs Node versions and npm/yarn/pnpm
- Pins versions in package.json (volta key)
- Switches toolchains automatically on cd
- Runs commands with the pinned tool (volta run)
- Fast, no shell hooks needed after setup

## When to Use

- Teams with mixed Node versions across projects
- Reproducible CI that matches local toolchains
- Replacing nvm churn in monorepos

## Real Commands

```bash
# Setup (once)
volta setup

# Install
volta install node
volta install node@20
volta install node@lts
volta install yarn@1.22.22
volta list-all node

# Pin per project
volta pin node@20
volta pin node@20.11.0 yarn@1.22.22

# Inspect
volta list
volta current
volta which node
volta run node --version

# Uninstall
volta uninstall node@16
```

## What Pinning Writes

```json
{
  "volta": {
    "node": "20.11.0",
    "yarn": "1.22.22"
  }
}
```

## Best Practices

- Pin exact versions, commit package.json changes
- Use volta run in CI to match local behavior
- Install npm/yarn alongside node with one command
- Use volta list-all before choosing versions
- Let CI install via volta install from pinned package.json

## Capabilities

### toolchain-install
Install Node.js versions and package managers.

**Commands:**
- `volta install node`
- `volta install node@20`
- `volta install node@lts npm@latest`
- `volta install yarn@1.22.22`
- `volta list-all node`
- `volta setup`

**Examples:**
- volta install node@20
- volta install node@lts npm@latest
- volta list-all node

### pinning-and-switching
Pin tool versions per project and switch automatically.

**Commands:**
- `volta pin node@20`
- `volta pin node@20.11.0 yarn@1.22.22`
- `volta list`
- `volta which node`
- `volta current`
- `volta uninstall node@16`

**Examples:**
- volta pin node@20
- volta pin node@20.11.0 yarn@1.22.22
- volta which node