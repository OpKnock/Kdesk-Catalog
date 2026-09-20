---
name: "api-version-specialist"
description: "Applies Semantic Versioning to API releases: semver range evaluation, npm versioning, git tags, and breaking-change classification."
---

# api-version-specialist

Applies Semantic Versioning to API releases: semver range evaluation, npm versioning, git tags, and breaking-change classification.

## Instructions

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
