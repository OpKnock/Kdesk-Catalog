---
name: "git-workflow"
description: "Designs and follows team git workflows (GitHub Flow, trunk-based, GitFlow): PR conventions, rebasing, conflict resolution, and remote hygiene. Use when working with pull request flow, trunk and history, devops or when the user mentions pull request flow, trunk and history, devops."
---

Designs and follows team git workflows (GitHub Flow, trunk-based, GitFlow): PR conventions, rebasing, conflict resolution, and remote hygiene.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `git fetch upstream && git rebase upstream/main`, `git pull --rebase`
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
