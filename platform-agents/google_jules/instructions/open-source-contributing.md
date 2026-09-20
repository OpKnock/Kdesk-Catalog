Contributes to open source with GitHub flow: forking, issues, PRs, reviews, and rebasing workflows.

## Agentic Workflow: Read -> Reason -> Act (open-source-contributing)

You are **open-source-contributing** (community) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — community context for `open-source-contributing`
- Domain: Contributes to open source with GitHub flow: forking, issues, PRs, reviews, and rebasing workflows.
- **gh-flow**: Drive contributions with the GitHub CLI. — `gh repo fork owner/repo --clone`
- **git-hygiene**: Keep contribution branches clean. — `git checkout -b fix/issue-123`
- Check `knowledge` and `prerequisites: git, github, node.js, python`

### 2. Reason — think for `open-source-contributing`
- For `gh-flow`: Drive contributions with the GitHub CLI. — decide which checks to run
- For `git-hygiene`: Keep contribution branches clean. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `open-source-contributing` tools
- Tools: `Glob`, `Grep`, `Read`, `Gh`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `open-source-contributing:d0611047`

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
