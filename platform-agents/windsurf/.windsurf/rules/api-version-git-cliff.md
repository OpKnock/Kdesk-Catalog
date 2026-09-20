---
trigger: glob
description: "Maintains API changelogs and version history: git-cliff generation from commits, conventional commits, and changelog-driven release notes. Use when working with git cliff, conventional commits or when the user mentions git cliff, conventional commits."
globs: ["**/*.r", "**/*.sh"]
---

Maintains API changelogs and version history: git-cliff generation from commits, conventional commits, and changelog-driven release notes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx git-cliff --init`, `npx commitizen init cz-conventional-changelog --save-dev --s`
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

# API Version v4 - Changelogs

Changelog generation and history.

## What This Skill Does
- Generates changelogs from commits
- Enforces conventional commits
- Produces release notes automatically

## When to Use
- Preparing release notes
- Auditing API changes between versions
- Enforcing commit standards

## Real Commands

```bash
npx git-cliff --init
npx git-cliff -o CHANGELOG.md
npx git-cliff --bump
npx commitizen init cz-conventional-changelog --save-dev --save-exact
```

## Conventional Commits

```
feat(users): add v2 avatar endpoint
fix(auth): correct token expiry check
BREAKING CHANGE: remove v1 legacy fields
```

## Testing
- Verify changelog entries per release
- Check breaking changes are flagged
- Test cliff config in CI


## Best Practices
- Enforce commit conventions with a linter
- Generate changelogs at release time
- Publish changelogs to docs sites

## Capabilities

### git-cliff
Generate changelogs from git history

**Parameters:**
- `tag` (string): Version tag to generate for
- `output` (string): Changelog output file
- `range` (string): Commit range

**Commands:**
- `npx git-cliff --init`
- `npx git-cliff -o CHANGELOG.md`
- `npx git-cliff --unreleased`
- `npx git-cliff --bump`
- `npx git-cliff --tag v2.0.0`

**Examples:**
- git-cliff --init creates cliff.toml
- git-cliff -o writes the changelog
- --unreleased previews pending changes

### conventional-commits
Structure commits for changelog generation

**Commands:**
- `npx commitizen init cz-conventional-changelog --save-dev --save-exact`
- `npx cz`
- `npx conventional-changelog -p angular -i CHANGELOG.md -s -r 0`
- `git log --oneline --format='%h %s' -20`

**Examples:**
- -cli --help
- -api --help

## References
- [git-cliff Docs](https://git-cliff.org/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
