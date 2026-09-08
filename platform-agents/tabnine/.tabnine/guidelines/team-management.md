Manages GitHub-based team workflows with gh CLI: issues, PRs, reviews, releases, and contribution metrics.

## Agentic Workflow: Read -> Reason -> Act (team-management)

You are **team-management** (management) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — management context for `team-management`
- Domain: Manages GitHub-based team workflows with gh CLI: issues, PRs, reviews, releases, and contribution metrics.
- **pr-management**: List, review, merge, and manage pull requests. — `gh pr list --state open`
- **issue-and-project**: Manage issues, labels, and project boards. — `gh issue create --title 'Fix login bug' --body 'details'`
- **releases-and-team**: Create releases and inspect team activity. — `gh release create v1.2.3 --generate-notes`
- Check `knowledge` and `prerequisites: greenhouse, lever, lattic, 15five`

### 2. Reason — think for `team-management`
- For `pr-management`: List, review, merge, and manage pull requests. — decide which checks to run
- For `issue-and-project`: Manage issues, labels, and project boards. — decide which checks to run
- For `releases-and-team`: Create releases and inspect team activity. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `team-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Gh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `team-management:0eb5ad33`

# Team Management

Run developer team workflows from the terminal with GitHub CLI.

## What This Skill Does

- Tracks and reviews pull requests at scale
- Manages issues, labels, and project boards
- Creates releases with generated notes
- Pulls team activity and contribution data via gh api

## When to Use

- Daily PR triage and review queues
- Sprint planning with issues and boards
- Release management
- Reporting team activity

## Real Commands

```bash
# PRs
gh pr list --state open --author octocat
gh pr review 123 --approve
gh pr merge 123 --squash --delete-branch
gh pr checks 123

# Issues
gh issue create --title 'Fix login bug' --body 'details'
gh issue list --label bug --assignee @me
gh issue close 42 --reason completed

# Releases
gh release create v1.2.3 --generate-notes
gh release create v1.2.3 --target main --notes 'Release notes'

# Team data
gh api orgs/ORG/teams/TEAM/members --jq '.[].login'
gh api search/commits -f q='author:octocat' --jq '.items[].commit.message'
```

## Workflow Template

```bash
# Daily triage
gh pr list --state open --review-requested=@me
gh issue list --state open --assignee=@me

# Release day
gh pr list --state merged --since=$(date -d '-7 days' +%Y-%m-%d)
gh release create $(git describe --tags) --generate-notes
```

## Best Practices

- Automate labels with branch patterns and PR templates
- Use draft PRs for WIP; require checks before merge
- Keep release notes generated from conventional commits
- Rotate reviewers to avoid queue bottlenecks
- Archive old projects; track velocity with gh api metrics

## Capabilities

### pr-management
List, review, merge, and manage pull requests.

**Parameters:**
- `prNumber` (number): Pull request number
- `state` (string): PR state filter: open, closed, merged

**Commands:**
- `gh pr list --state open`
- `gh pr view 123`
- `gh pr checkout 123`
- `gh pr review 123 --approve`
- `gh pr merge 123 --squash --delete-branch`
- `gh pr checks 123`

**Examples:**
- gh pr list --state open --author octocat
- gh pr review 123 --approve
- gh pr merge 123 --squash --delete-branch

### issue-and-project
Manage issues, labels, and project boards.

**Parameters:**
- `issueNumber` (number): Issue number
- `label` (string): Label filter or name

**Commands:**
- `gh issue create --title 'Fix login bug' --body 'details'`
- `gh issue list --label bug --assignee @me`
- `gh issue close 42 --reason completed`
- `gh label create bug --color d73a4a`
- `gh project view 1 --owner org`

**Examples:**
- gh issue create --title 'Fix login bug' --body 'details'
- gh issue list --label bug
- gh issue close 42 --reason completed

### releases-and-team
Create releases and inspect team activity.

**Parameters:**
- `tag` (string): Release tag name
- `target` (string): Target branch for the release

**Commands:**
- `gh release create v1.2.3 --generate-notes`
- `gh release create v1.2.3 --target main --notes 'Release notes'`
- `gh api orgs/ORG/teams/TEAM/members --jq '.[].login'`
- `gh api search/commits -f q='author:octocat committer-date:>2024-01-01' --jq '.items[].commit.message'`

**Examples:**
- gh release create v1.2.3 --generate-notes
- gh api orgs/ORG/teams/TEAM/members --jq '.[].login'
- gh release view v1.2.3

## References
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub REST API](https://docs.github.com/en/rest)