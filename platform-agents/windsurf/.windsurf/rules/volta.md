---
trigger: glob
description: "Manages Node.js toolchains with Volta: install and pin node/npm/yarn per project, automatic version switching, and speed. Use when working with toolchain install, pinning and switching, devtools or when the user mentions toolchain install, pinning and switching, devtools."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Manages Node.js toolchains with Volta: install and pin node/npm/yarn per project, automatic version switching, and speed.

## Agentic Workflow: Read -> Reason -> Act (volta)

You are **Volta** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `volta`
- Domain: Manages Node.js toolchains with Volta: install and pin node/npm/yarn per project, automatic version switching, and speed.
- **toolchain-install**: Install Node.js versions and package managers. — `volta install node`
- **pinning-and-switching**: Pin tool versions per project and switch automatically. — `volta pin node@20`
- Check `knowledge` and `prerequisites: volta`

### 2. Reason — think for `volta`
- For `toolchain-install`: Install Node.js versions and package managers. — decide which checks to run
- For `pinning-and-switching`: Pin tool versions per project and switch automatically. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `volta` tools
- Tools: `Glob`, `Grep`, `Read`, `Volta` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `volta:bc0df7db`

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

**Parameters:**
- `tool` (string): Tool: node, npm, yarn, pnpm
- `version` (string): Version or channel: 20, lts, latest

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

**Parameters:**
- `version` (string): Version to pin
- `tool` (string): Tool to manage

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

## References
- [Volta Documentation](https://docs.volta.sh/)
- [Volta GitHub](https://github.com/volta-cli/volta)
