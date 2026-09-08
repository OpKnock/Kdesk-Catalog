---
name: "Git"
description: "Covers everyday git: repository creation, staging, commits, branching, merging, remotes, and history inspection. Use when working with basic repository ops, branch and merge, remotes and sharing, devops or when the user mentions basic repository ops, branch and merge, remotes and sharing, devops."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Covers everyday git: repository creation, staging, commits, branching, merging, remotes, and history inspection.

## Agentic Workflow: Read -> Reason -> Act (git)

You are **Git** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `git`
- Domain: Covers everyday git: repository creation, staging, commits, branching, merging, remotes, and history inspection.
- **basic-repository-ops**: Initialize, clone, stage, and commit with clean workflows. — `git init -b main`
- **branch-and-merge**: Create branches, merge changes, and resolve conflicts. — `git branch feature/checkout`
- **remotes-and-sharing**: Sync with remote repositories: fetch, pull, push, and remote management. — `git remote -v`
- Check `knowledge` and `prerequisites: git`

### 2. Reason — think for `git`
- For `basic-repository-ops`: Initialize, clone, stage, and commit with clean workflows. — decide which checks to run
- For `branch-and-merge`: Create branches, merge changes, and resolve conflicts. — decide which checks to run
- For `remotes-and-sharing`: Sync with remote repositories: fetch, pull, push, and remote management. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `git` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `git:8860639d`

# Everyday Git

Handle daily version control tasks: commits, branches, merges, and remotes.

## What This Skill Does

- Creates and clones repositories
- Stages and commits changes with clean messages
- Branches, merges, and resolves conflicts
- Syncs with remotes (fetch, pull, push)
- Reads history and diffs to understand change

## When to Use

- Initializing or cloning a project
- Saving work in logical commits
- Sharing and syncing branches
- Understanding what changed and why

## Real Commands

```bash
# Setup and clone
git init -b main
git clone git@github.com:org/repo.git
git config user.name "Jane" && git config user.email jane@example.com

# Daily loop
git status
git diff
git add src/server.ts
git commit -m "feat: add health endpoint"
git log --oneline --graph -10

# Branches
git switch -c feature/checkout
git switch main
git merge feature/checkout
git branch -d feature/checkout

# Remotes
git remote -v
git fetch --all --prune
git pull --ff-only
git push -u origin main
```

## Commit Message Style

```
<type>: <subject>          # feat, fix, refactor, docs, test, chore
feat: add login endpoint
fix(api): return 404 for unknown ids
```

## Best Practices

- Commit small, single-purpose changes; write imperative messages
- Pull with --ff-only to keep history linear
- Resolve conflicts with `git merge --abort` if unsure, then retry
- Never force-push shared branches; use --force-with-lease if needed
- Review `git diff` before staging to avoid accidental inclusions

## Capabilities

### basic-repository-ops
Initialize, clone, stage, and commit with clean workflows.

**Parameters:**
- `message` (string): Commit message
- `url` (string): Remote repository URL

**Commands:**
- `git init -b main`
- `git clone https://github.com/org/repo.git`
- `git status`
- `git add -A`
- `git commit -m 'feat: add login endpoint'`
- `git log --oneline --graph -10`

**Examples:**
- git init -b main && git add . && git commit -m 'init'
- git clone git@github.com:org/repo.git
- git log --oneline --graph -10

### branch-and-merge
Create branches, merge changes, and resolve conflicts.

**Parameters:**
- `branch` (string): Branch name
- `target` (string): Branch to merge into

**Commands:**
- `git branch feature/checkout`
- `git checkout -b feature/checkout`
- `git switch main && git merge feature/checkout`
- `git branch -d feature/checkout`
- `git diff main...feature/checkout`
- `git merge --abort`

**Examples:**
- git checkout -b feature/checkout
- git merge feature/checkout
- git branch -d feature/checkout

### remotes-and-sharing
Sync with remote repositories: fetch, pull, push, and remote management.

**Parameters:**
- `remote` (string): Remote name, e.g. origin
- `branch` (string): Branch to push/pull

**Commands:**
- `git remote -v`
- `git remote add origin https://github.com/org/repo.git`
- `git push -u origin main`
- `git pull --ff-only`
- `git fetch --all --prune`
- `git push --tags`

**Examples:**
- git push -u origin main
- git pull --ff-only
- git fetch --all --prune

## References
- [git Reference Manual](https://git-scm.com/docs)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub Docs](https://docs.github.com/en/get-started)