# Api Sdk Changesets

Manages SDK versioning and releases with changesets: change tracking, version bumps, changelogs, and semantic-release automation.

## Instructions

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
