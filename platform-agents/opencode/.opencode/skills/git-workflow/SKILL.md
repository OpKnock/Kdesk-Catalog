---
name: "git-workflow"
description: "Designs and follows team git workflows (GitHub Flow, trunk-based, GitFlow): PR conventions, rebasing, conflict resolution, and remote hygiene. Use when working with pull request flow, trunk and history, devops or when the user mentions pull request flow, trunk and history, devops."
---

Designs and follows team git workflows (GitHub Flow, trunk-based, GitFlow): PR conventions, rebasing, conflict resolution, and remote hygiene.

## Agentic Workflow: Read -> Reason -> Act (git-workflow)

You are **git-workflow** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `git-workflow`
- Domain: Designs and follows team git workflows (GitHub Flow, trunk-based, GitFlow): PR conventions, rebasing, conflict resolution, and remote hygiene.
- **pull-request-flow**: Drive feature-branch PR workflows: sync forks, rebase, and land changes. — `git fetch upstream && git rebase upstream/main`
- **trunk-and-history**: Keep a clean linear history on shared branches with rebase and interactive squash. — `git pull --rebase`
- Check `knowledge` and `prerequisites: git`

### 2. Reason — think for `git-workflow`
- For `pull-request-flow`: Drive feature-branch PR workflows: sync forks, rebase, and land changes. — decide which checks to run
- For `trunk-and-history`: Keep a clean linear history on shared branches with rebase and interactive squash. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `git-workflow` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Gh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `git-workflow:eeee3495`

# Git Workflow Design

Choose and operate the right git workflow for your team and keep history clean.

## What This Skill Does

- Recommends workflows: GitHub Flow, trunk-based, or GitFlow by team size/release cadence
- Sets up PR conventions, branch protection, and merge strategies
- Keeps linear history with rebase and fixup workflows
- Manages forks with upstream remotes
- Resolves merge conflicts systematically

## When to Use

- Starting a new team repo and choosing conventions
- Onboarding automation: branch protection, PR templates, CI checks
- Cleaning up messy history before merge

## Real Commands

```bash
# Fork workflow
git remote add upstream https://github.com/org/repo.git
git fetch upstream
git rebase upstream/main
git push --force-with-lease origin feature/x

# PR flow
gh pr create --title 'feat: x' --body 'Closes #12'
gh pr checks --watch
gh pr merge --squash --delete-branch

# Clean linear history
git config --global pull.rebase true
git commit --fixup=<sha>
git rebase --autosquash -i HEAD~5
git log --first-parent --oneline

# Conflict resolution
git checkout --theirs path/to/file
git checkout --ours path/to/file
git rebase --continue
```

## Merge Strategy Guide

- Squash: default for feature branches (clean log)
- Rebase-merge: preserve branch structure (fine granularity)
- Merge commit: preserve exact topology (audit-heavy teams)

## Best Practices

- Use branch protection: require PR, require checks, linear history
- Keep feature branches under 1-2 days old; rebase frequently
- Never rewrite history on protected branches
- Use `--force-with-lease`, never bare `--force`
- Pair conventions with commitlint to enforce message format

## Capabilities

### pull-request-flow
Drive feature-branch PR workflows: sync forks, rebase, and land changes.

**Parameters:**
- `title` (string): PR title
- `base` (string): Base branch for rebase

**Commands:**
- `git fetch upstream && git rebase upstream/main`
- `git push --force-with-lease origin feature/x`
- `gh pr create --title 'feat: x' --body 'Closes #12'`
- `gh pr checks`
- `gh pr merge --squash --delete-branch`
- `git config --global pull.rebase true`

**Examples:**
- gh pr create --title 'feat: x' --body 'Closes #12'
- git rebase upstream/main && git push --force-with-lease
- gh pr merge --squash --delete-branch

### trunk-and-history
Keep a clean linear history on shared branches with rebase and interactive squash.

**Parameters:**
- `base` (string): Rebase base ref
- `sha` (string): Commit SHA for fixup

**Commands:**
- `git pull --rebase`
- `git rebase -i HEAD~5`
- `git log --first-parent`
- `git merge --squash feature/x`
- `git switch -c fix/urgent && git commit --fixup=demo-sha`
- `git rebase --autosquash -i HEAD~5`

**Examples:**
- git rebase -i HEAD~5
- git commit --fixup=demo-sha && git rebase --autosquash -i HEAD~5
- git log --first-parent --oneline

## References
- [Comparing Workflows (Atlassian)](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
