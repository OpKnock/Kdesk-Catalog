Generate conventional changelogs from git history using git-cliff and conventional-changelog, with semantic-release ready config.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `git-cliff --init`, `npx conventional-changelog -p angular -i CHANGELOG.md -s -r `
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