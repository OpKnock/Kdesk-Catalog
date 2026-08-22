---
name: "changelog-generation"
description: "Generate conventional changelogs from git history using git-cliff and conventional-changelog, with semantic-release ready config."
type: knowledge
triggers: ["changelog-generation", "git-cliff", "conventional-changelog"]
---

# Changelog Generation

Generate conventional changelogs from git history using git-cliff and conventional-changelog, with semantic-release ready config.

## Instructions

# Changelog Generation

Generate release changelogs from git history automatically.

## When to Use

- Preparing release notes before tagging
- Keeping a changelog in sync with conventional commits
- Automating versioning in CI

## Setup

```bash
cargo install git-cliff
# or via scoop/choco on Windows
scoop install git-cliff
```

## git-cliff

```bash
git-cliff --init
# edit cliff.toml to add a GitHub remote for links
git-cliff -o CHANGELOG.md
git-cliff --unreleased -o CHANGELOG.md
git-cliff --bump --tag v1.2.0 -o CHANGELOG.md
```

## conventional-changelog

```bash
npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0
npx standard-version --dry-run
npx standard-version
npx standard-version --release-as 1.3.0
```

## Commit Convention

```
feat: add retry middleware
fix(api): return 404 for unknown routes
feat(api)!: remove legacy /v1/status endpoint
docs: update README
```

Breaking changes use `!` or a `BREAKING CHANGE:` footer and trigger major bumps.

## Testing

```bash
# Dry run to review what would be released and its changelog
npx standard-version --dry-run
# Regenerate from scratch
npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0
```

## Best Practices

- Enforce conventional commits in CI with commitlint
- Generate changelogs in CI on the release tag
- Commit CHANGELOG.md before tagging
- Use --dry-run before standard-version releases

## Capabilities

### git-cliff
Generate changelogs from git commits using git-cliff with configurable templates

**Commands:**
- `git-cliff --init`
- `git-cliff -o CHANGELOG.md`
- `git-cliff --unreleased -o CHANGELOG.md`
- `git-cliff --bump --unreleased --prepend CHANGELOG.md`

**Examples:**
- git-cliff --init && git-cliff -o CHANGELOG.md
- git-cliff --unreleased -o CHANGELOG.md
- git-cliff --bump --tag v1.2.0 -o CHANGELOG.md

### conventional-changelog
Generate and update changelogs with the conventional-changelog CLI and standard-version

**Commands:**
- `npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0`
- `npx conventional-changelog -p conventionalcommits -i CHANGELOG.md -s`
- `npx standard-version`
- `npx standard-version --release-as 1.3.0`

**Examples:**
- npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0
- npx standard-version --dry-run
- npx standard-version --release-as major
