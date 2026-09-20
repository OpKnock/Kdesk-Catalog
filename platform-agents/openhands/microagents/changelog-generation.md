---
name: "changelog-generation"
description: "Generate conventional changelogs from git history using git-cliff and conventional-changelog, with semantic-release ready config. Use when working with git cliff, conventional changelog, api or when the user mentions git cliff, conventional changelog, api."
type: knowledge
triggers: ["changelog-generation", "git-cliff", "conventional-changelog"]
---

Generate conventional changelogs from git history using git-cliff and conventional-changelog, with semantic-release ready config.

## Agentic Workflow: Read -> Reason -> Act (changelog-generation)

You are **Changelog Generation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `changelog-generation`
- Domain: Generate conventional changelogs from git history using git-cliff and conventional-changelog, with semantic-release ready config.
- **git-cliff**: Generate changelogs from git commits using git-cliff with configurable templates — `git-cliff --init`
- **conventional-changelog**: Generate and update changelogs with the conventional-changelog CLI and standard-version — `npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0`
- Check `knowledge` and `prerequisites: git-cliff, npx`

### 2. Reason — think for `changelog-generation`
- For `git-cliff`: Generate changelogs from git commits using git-cliff with configurable templates — decide which checks to run
- For `conventional-changelog`: Generate and update changelogs with the conventional-changelog CLI and standard-version — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `changelog-generation` tools
- Tools: `Glob`, `Grep`, `Read`, `Git-cliff`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `changelog-generation:c1045295`

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

**Parameters:**
- `tag` (string): Version tag to release, e.g. v1.2.0
- `output` (string): Changelog output file, default CHANGELOG.md

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

**Parameters:**
- `preset` (string): Commit convention preset: angular, conventionalcommits, eslint
- `release_as` (string): Force version bump level: major, minor, patch, or explicit version

**Commands:**
- `npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0`
- `npx conventional-changelog -p conventionalcommits -i CHANGELOG.md -s`
- `npx standard-version`
- `npx standard-version --release-as 1.3.0`

**Examples:**
- npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0
- npx standard-version --dry-run
- npx standard-version --release-as major

## References
- [git-cliff Documentation](https://git-cliff.org/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/)
