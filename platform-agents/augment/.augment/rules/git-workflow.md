---
type: agent_requested
description: "Designs and follows team git workflows (GitHub Flow, trunk-based, GitFlow): PR conventions, rebasing, conflict resolution, and remote hygiene."
---

# git-workflow

Designs and follows team git workflows (GitHub Flow, trunk-based, GitFlow): PR conventions, rebasing, conflict resolution, and remote hygiene.

## Instructions

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