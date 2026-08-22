---
name: "open-source-contributing"
description: "Contributes to open source with GitHub flow: forking, issues, PRs, reviews, and rebasing workflows."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# open-source-contributing

Contributes to open source with GitHub flow: forking, issues, PRs, reviews, and rebasing workflows.

## Instructions

# Open Source Contributing

Make quality contributions without stepping on maintainers.

## When to Use

- Finding and fixing issues in upstream projects
- Submitting features and docs
- Reviewing others' PRs

## Find work

```bash
gh issue list --repo owner/repo --label 'good first issue'
gh issue view 123 --repo owner/repo
```

Read CONTRIBUTING.md and the issue thread before starting.

## Fork and branch

```bash
gh repo fork owner/repo --clone
git checkout -b fix/issue-123
```

## Small commits, clear messages

```bash
git add .
git commit -m 'Fix: handle empty query in search (fixes #123)'
git push -u origin fix/issue-123
```

## Open the PR

```bash
gh pr create --title 'Fix #123: handle empty query' --body 'Closes #123'
```

Reference issues with Closes/Fixes so they auto-close.

## Keep in sync

```bash
git fetch upstream && git rebase upstream/main
git push --force-with-lease
```

Never force-push without -with-lease.

## Responding to review

- Address feedback in follow-up commits.
- Request re-review when done.
- Push commit count down where maintainers prefer squashes.

## Best practices

- One logical change per PR.
- Run the project's lint/tests before pushing.
- Respect maintainer review cadence - be patient.
- Add tests with fixes; maintainers value them.

## Testing

```bash
npm test
npx eslint . --max-warnings 0
```

Pass the project's own checks before opening the PR.

## Capabilities

### gh-flow
Drive contributions with the GitHub CLI.

**Commands:**
- `gh repo fork owner/repo --clone`
- `gh issue list --repo owner/repo --label 'good first issue'`
- `gh issue view 123 --repo owner/repo`
- `gh pr create --title 'Fix #123: ...' --body 'Closes #123'`
- `gh pr checkout 456`

**Examples:**
- gh repo fork owner/repo --clone --remote=true
- gh issue list --repo owner/repo --search 'label:"good first issue" is:open' --limit 20
- gh pr create --title 'Add caching to API' --body 'Closes #88' --draft

### git-hygiene
Keep contribution branches clean.

**Commands:**
- `git checkout -b fix/issue-123`
- `git fetch upstream && git rebase upstream/main`
- `git rebase -i HEAD~3`
- `git log --oneline origin/main..HEAD`
- `git push --force-with-lease origin fix/issue-123`

**Examples:**
- git fetch upstream && git rebase upstream/main && git push --force-with-lease
- git commit --amend --no-edit
- git log --oneline --graph --decorate -10