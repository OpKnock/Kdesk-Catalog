---
name: "git-flow"
description: "Applies the GitFlow branching model with git-flow extensions: features, releases, hotfixes, and support branches. Use when working with feature branches, releases and hotfixes, devops or when the user mentions feature branches, releases and hotfixes, devops."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Applies the GitFlow branching model with git-flow extensions: features, releases, hotfixes, and support branches.

## Agentic Workflow: Read -> Reason -> Act (git-flow)

You are **git-flow** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `git-flow`
- Domain: Applies the GitFlow branching model with git-flow extensions: features, releases, hotfixes, and support branches.
- **feature-branches**: Start, finish, and publish feature branches under git-flow. — `git flow feature start login-passwordless`
- **releases-and-hotfixes**: Cut releases from develop and patch production from master/main. — `git flow release start 1.2.0`
- Check `knowledge` and `prerequisites: git`

### 2. Reason — think for `git-flow`
- For `feature-branches`: Start, finish, and publish feature branches under git-flow. — decide which checks to run
- For `releases-and-hotfixes`: Cut releases from develop and patch production from master/main. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `git-flow` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `git-flow:a19d0550`

# GitFlow Branching Model

Structure development around feature, release, and hotfix branches with git-flow.

## What This Skill Does

- Initializes the git-flow branch structure (develop + master/main)
- Manages feature branches off develop
- Prepares releases off develop with freeze windows
- Fixes production with hotfix branches off main, merged back into both
- Handles support branches for legacy versions

## When to Use

- Teams on scheduled releases (not continuous deployment)
- Projects needing a stable main + active develop line
- When hotfixes must bypass the develop queue

## Real Commands

```bash
# Initialize
git flow init -d

# Features
git flow feature start login-passwordless
git flow feature publish login-passwordless
git flow feature finish login-passwordless
git flow feature list

# Releases
git flow release start 1.2.0
git flow release publish 1.2.0
git flow release finish 1.2.0 -m 'Release 1.2.0'

# Hotfixes
git flow hotfix start 1.2.1
git flow hotfix finish 1.2.1 -m 'Hotfix 1.2.1'
```

## Branch Flow

```
feature/*   -> develop
develop     -> release/x.y.z -> main (tag x.y.z)
hotfix/x.y  -> main + develop
support/x.y -> off main
```

## Best Practices

- Finish releases/hotfixes with `-m` to create annotated tags
- Never commit directly to develop or main; always via flow commands or PRs
- Publish feature branches early for backup and review
- Use `git flow release start` only when the release scope is frozen
- Prefer GitHub Flow for continuous-delivery teams; GitFlow suits calendar releases

## Capabilities

### feature-branches
Start, finish, and publish feature branches under git-flow.

**Parameters:**
- `name` (string): Feature branch name
- `origin` (string): Remote to sync with

**Commands:**
- `git flow feature start login-passwordless`
- `git flow feature publish login-passwordless`
- `git flow feature finish login-passwordless`
- `git flow feature list`
- `git flow feature pull origin login-passwordless`

**Examples:**
- git flow feature start login-passwordless
- git flow feature publish login-passwordless
- git flow feature finish login-passwordless

### releases-and-hotfixes
Cut releases from develop and patch production from master/main.

**Parameters:**
- `version` (string): Release or hotfix version tag
- `message` (string): Tag message on finish

**Commands:**
- `git flow release start 1.2.0`
- `git flow release publish 1.2.0`
- `git flow release finish 1.2.0 -m 'Release 1.2.0'`
- `git flow hotfix start 1.2.1`
- `git flow hotfix finish 1.2.1`
- `git flow init`

**Examples:**
- git flow release start 1.2.0
- git flow release finish 1.2.0 -m 'Release 1.2.0'
- git flow hotfix finish 1.2.1

## References
- [GitFlow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [A Successful Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [gitflow-avh](https://github.com/petervanderdoes/gitflow-avh)