---
type: agent_requested
description: "Manages SDK versioning and releases with changesets: change tracking, version bumps, changelogs, and semantic-release automation. Use when working with changesets, semantic release or when the user mentions changesets, semantic release."
---

Manages SDK versioning and releases with changesets: change tracking, version bumps, changelogs, and semantic-release automation.

## Agentic Workflow: Read -> Reason -> Act (api-sdk-changesets)

You are **Api Sdk Changesets** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-sdk-changesets`
- Domain: Manages SDK versioning and releases with changesets: change tracking, version bumps, changelogs, and semantic-release automation.
- **changesets**: Track SDK changes with changesets — `npx @changesets/cli init`
- **semantic-release**: Automate releases from commit messages — `npx semantic-release --dry-run`
- Check `knowledge` and `prerequisites: openapi-generator, node.js, python`

### 2. Reason — think for `api-sdk-changesets`
- For `changesets`: Track SDK changes with changesets — decide which checks to run
- For `semantic-release`: Automate releases from commit messages — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-sdk-changesets` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-sdk-changesets:1327c3ef`

# API SDK v5 - Releases

SDK versioning and release automation.

## What This Skill Does
- Tracks changes with changesets
- Bumps versions and writes changelogs
- Automates publishing with semantic-release

## When to Use
- Multi-package SDK releases
- Enforcing semver discipline
- Automating npm publishing

## Real Commands

```bash
npx @changesets/cli init
npx changeset
npx changeset version
npx changeset publish
npx semantic-release --dry-run
```

## Changeset Flow
1. Author changes: npx changeset
2. Version: npx changeset version
3. Publish: npx changeset publish

## Testing
- Run version bumps in a dry run
- Verify changelog entries per release
- Test publish on a canary tag

## Best Practices
- Require changesets for all PRs
- Use semver ranges intentionally
- Automate release notes from changelogs

## Capabilities

### changesets
Track SDK changes with changesets

**Parameters:**
- `semver` (string): major, minor, or patch bump
- `package` (string): Package to release
- `tag` (string): npm dist-tag

**Commands:**
- `npx @changesets/cli init`
- `npx changeset`
- `npx changeset version`
- `npx changeset status`
- `npx changeset publish`

**Examples:**
- npx changeset adds a changeset file
- changeset version bumps versions and changelogs
- changeset publish releases to npm

### semantic-release
Automate releases from commit messages

**Commands:**
- `npx semantic-release --dry-run`
- `npx semantic-release`
- `npm version major`
- `git tag -a v2.0.0 -m 'SDK v2.0.0'`

**Examples:**
- -cli --help
- -api --help

## References
- [Changesets](https://github.com/changesets/changesets)
- [Semantic Release](https://semantic-release.gitbook.io/)