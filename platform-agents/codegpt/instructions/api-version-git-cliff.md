# Api Version Git Cliff

Maintains API changelogs and version history: git-cliff generation from commits, conventional commits, and changelog-driven release notes.

## Instructions

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
