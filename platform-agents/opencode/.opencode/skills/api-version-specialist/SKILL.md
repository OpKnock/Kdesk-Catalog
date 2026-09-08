---
name: "api-version-specialist"
description: "Applies Semantic Versioning to API releases: semver range evaluation, npm versioning, git tags, and breaking-change classification. Use when working with semver tools, breaking classification or when the user mentions semver tools, breaking classification."
---

Applies Semantic Versioning to API releases: semver range evaluation, npm versioning, git tags, and breaking-change classification.

## Agentic Workflow: Read -> Reason -> Act (api-version-specialist)

You are **api-version-specialist** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-version-specialist`
- Domain: Applies Semantic Versioning to API releases: semver range evaluation, npm versioning, git tags, and breaking-change classification.
- **semver-tools**: Evaluate and apply semver versions — `npx semver 1.2.3 major`
- **breaking-classification**: Classify changes as breaking or non-breaking — `npm version major -m "chore: release v%s"`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-version-specialist`
- For `semver-tools`: Evaluate and apply semver versions — decide which checks to run
- For `breaking-classification`: Classify changes as breaking or non-breaking — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-version-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-version-specialist:ba68c06b`

# API Version Specialist

SemVer discipline for API releases.

## What This Skill Does
- Applies semver rules to version numbers
- Automates version bumps and tags
- Classifies breaking changes correctly

## When to Use
- Planning major version releases
- Automating release versioning
- Auditing version histories

## Real Commands

```bash
npx semver 1.2.3 major
npm version minor -m "chore: release %s"
git tag -l 'v*' --sort=-v:refname | head
```

## SemVer Rules
- MAJOR: breaking changes
- MINOR: backward-compatible features
- PATCH: backward-compatible fixes

## Testing
- Verify range evaluations with npx semver
- Check tags match npm versions
- Review changelogs against bump type


## Best Practices
- Never break compatibility in minor releases
- Document breaking changes prominently
- Automate tagging in release pipelines

## Capabilities

### semver-tools
Evaluate and apply semver versions

**Parameters:**
- `version` (string): Current version
- `bump` (string): major, minor, or patch
- `range` (string): Semver range expression

**Commands:**
- `npx semver 1.2.3 major`
- `npx semver "1.2.3" -r ">=1.0.0 <2.0.0"`
- `npm version patch`
- `npm version minor -m "chore: release %s"`
- `git tag -l 'v*' --sort=-v:refname | head`

**Examples:**
- npx semver 1.2.3 major returns 2.0.0
- -r evaluates range membership
- npm version patch tags and bumps

### breaking-classification
Classify changes as breaking or non-breaking

**Commands:**
- `npm version major -m "chore: release v%s"`
- `git tag -a v2.0.0 -m 'Breaking: remove legacy fields'`
- `npm view my-api versions --json`
- `git log --oneline v1.0.0..HEAD`

**Examples:**
- -cli --help
- -api --help

## References
- [Semantic Versioning Spec](https://semver.org/)
- [npm version Command](https://docs.npmjs.com/cli/v10/commands/npm-version)
