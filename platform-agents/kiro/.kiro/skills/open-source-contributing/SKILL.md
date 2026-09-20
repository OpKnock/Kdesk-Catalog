---
name: "open-source-contributing"
description: "Contributes to open source with GitHub flow: forking, issues, PRs, reviews, and rebasing workflows. Use when working with gh flow, git hygiene or when the user mentions gh flow, git hygiene."
license: "MIT"
compatibility: "Requires git, github, node.js, python, first-timers."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "community"}
allowed-tools: "Glob Grep Read Bash(gh:*) Bash(git:*)"
---

Contributes to open source with GitHub flow: forking, issues, PRs, reviews, and rebasing workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh repo fork owner/repo --clone`, `git checkout -b fix/issue-123`
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

**Parameters:**
- `repo` (string): owner/repo
- `label` (string): Issue label filter
- `issue` (number): Issue number

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

**Parameters:**
- `branch` (string): Feature branch name
- `upstream` (string): Upstream remote name
- `base` (string): Base branch for logs

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

## References
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [GitHub CLI](https://cli.github.com/manual/)
- [Contributing guide](https://opensource.guide/how-to-contribute/)
