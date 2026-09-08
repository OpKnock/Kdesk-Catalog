---
trigger: glob
description: "Manages projects with GitHub Projects and CLI trackers: issue planning, sprint views, and status automation via gh. Use when working with github projects, tracking or when the user mentions github projects, tracking."
globs: ["**/*.r", "**/*.sh"]
---

Manages projects with GitHub Projects and CLI trackers: issue planning, sprint views, and status automation via gh.

## Agentic Workflow: Read -> Reason -> Act (project-management)

You are **project-management** (management) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — management context for `project-management`
- Domain: Manages projects with GitHub Projects and CLI trackers: issue planning, sprint views, and status automation via gh.
- **github-projects**: Plan and track work with GitHub Projects. — `gh project list --owner @me`
- **tracking**: Manage issues, milestones, and sprints. — `gh issue list --repo owner/repo --state open --label bug`
- Check `knowledge` and `prerequisites: jira, asana, linear, github`

### 2. Reason — think for `project-management`
- For `github-projects`: Plan and track work with GitHub Projects. — decide which checks to run
- For `tracking`: Manage issues, milestones, and sprints. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `project-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Gh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `project-management:5147b6b5`

# Project Management

Run sprints with trackable, automatable artifacts.

## When to Use

- Sprint planning and backlog grooming
- Cross-team status visibility
- Release tracking with milestones

## Plan with Projects

```bash
gh project list --owner @me
gh project view 1 --owner @me
gh issue create --title 'Add caching layer' --project 1 --label enhancement
```

## Sprint cadence

- Plan: move ready issues into the sprint milestone.
- Daily: check `gh issue list --assignee @me`.
- Close: close completed with reason completed.
- Retro: review cycle time from issue history.

## Milestones as sprints

```bash
gh issue edit 42 --repo owner/repo --milestone 'Sprint 24'
gh api repos/{owner}/{repo}/milestones -q '.[] | {title, open_issues}'
```

## Status automation

Wire Project item status to PR/issue events: closed -> Done, PR review requested -> In Review.

## Best practices

- Every task: one issue with acceptance criteria.
- Labels encode priority and type, not emotion.
- Keep Status views filtered by team to avoid noise.
- Review project metrics (cycle time, WIP) each retro.

## Testing

Audit that all open milestone issues have assignees and acceptance criteria.

## Capabilities

### github-projects
Plan and track work with GitHub Projects.

**Parameters:**
- `project` (number): Project number
- `owner` (string): Project owner: @me or org
- `label` (string): Issue labels, comma-separated

**Commands:**
- `gh project list --owner @me`
- `gh project view 1 --owner @me`
- `gh issue create --title 'Add caching layer' --body 'Context...' --project 1 --label enhancement`
- `gh project item-add 1 --owner @me --url https://github.com/owner/repo/issues/42`
- `gh project item-edit 1 --owner @me --id PVTI_123 --field Status --project-number 1`

**Examples:**
- gh project list --owner org-name
- gh issue create --title 'Fix checkout bug' --project 1 --label bug,sev2
- gh project view 1 --owner @me --field Status | head -20

### tracking
Manage issues, milestones, and sprints.

**Parameters:**
- `milestone` (string): Milestone title
- `repo` (string): owner/repo
- `assignee` (string): Issue assignee filter

**Commands:**
- `gh issue list --repo owner/repo --state open --label bug`
- `gh issue edit 42 --repo owner/repo --milestone 'Sprint 24'`
- `gh issue close 42 --repo owner/repo --reason completed`
- `gh api repos/{owner}/{repo}/milestones -q '.[] | {title, open_issues}'`
- `gh issue list --repo owner/repo --assignee @me --state open`

**Examples:**
- gh issue list --repo owner/repo --search 'label:bug is:open sort:created-asc'
- gh issue edit 42 --repo owner/repo --add-label 'in-review'
- gh api repos/{owner}/{repo}/milestones --jq '.[].title'

## References
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub CLI manual](https://cli.github.com/manual/)
- [Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
