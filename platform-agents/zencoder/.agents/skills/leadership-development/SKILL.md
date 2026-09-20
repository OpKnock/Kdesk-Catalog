---
name: "leadership-development"
description: "Develops engineering leaders: PR review practice, contribution metrics, and team-level operational habits grounded in real GitHub workflows. Use when working with review practice, team habits or when the user mentions review practice, team habits."
license: "MIT"
compatibility: "Requires lattic, 15five, slack, zoom, greenhouse."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "management"}
allowed-tools: "Glob Grep Read Bash(gh:*)"
---

Develops engineering leaders: PR review practice, contribution metrics, and team-level operational habits grounded in real GitHub workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh pr list --repo owner/repo --search 'reviewed-by:@me' --st`, `gh issue create --title '1:1 notes - 2026-08-10' --body 'Ski`
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

# Leadership Development

Build measurable leadership habits with tangible artifacts.

## When to Use

- New leads establishing review and 1:1 cadence
- Tracking team health and contribution trends
- Converting feedback into tracked action items

## Review practice

```bash
gh pr list --review-requested @me --state open
gh pr diff 123 --repo owner/repo | wc -l
```

Keep a review budget: every open request gets a response within one business day.

## 1:1s with artifacts

Create an issue per 1:1 with a shared template:

```bash
gh issue create --title '1:1 notes - 2026-08-10' --body 'Skip: roadmap; focus: growth areas' --label 1-1
gh issue list --label 1-1 --state open
```

Follow-ups become tracked issues, not conversational memory.

## Team metrics

```bash
gh api repos/{owner}/{repo}/stats/participation | jq '.all'
gh api repos/{owner}/{repo}/contributors -q '.[:10][] | {login, contributions}'
```

Use trends (not snapshots) to spot burnout or bus-factor risk.

## Feedback mechanics

- Specific: cite the PR/commit, not a vibe.
- Timely: within the same week.
- Balanced: behavior and impact, with a concrete ask.
- Tracked: every feedback item becomes an action item.

## Best practices

- Protect focus time; reviews are a queue, not an inbox.
- Rotate incident leadership so everyone practices command.
- Run a lightweight retrospective cadence (2 weeks).
- Publish team norms as docs, review quarterly.

## Testing

Audit your own habits monthly: review response time, 1:1 cadence, action-item closure rate.

## Capabilities

### review-practice
Build review habits and track team contribution patterns.

**Parameters:**
- `repo` (string): owner/repo pair
- `reviewed-by` (string): Reviewer login filter
- `search` (string): GitHub search query

**Commands:**
- `gh pr list --repo owner/repo --search 'reviewed-by:@me' --state all`
- `gh pr list --review-requested @me`
- `gh api repos/{owner}/{repo}/stats/participation | jq '.all'`
- `gh api repos/{owner}/{repo}/contributors -q '.[] | {login, contributions}'`
- `gh pr diff 123 --repo owner/repo | wc -l`

**Examples:**
- gh pr list --repo owner/repo --search 'reviewed-by:@me created:>=2026-07-01'
- gh api repos/{owner}/{repo}/contributors -q '.[:10][] | {login, contributions}'
- gh pr list --review-requested @me --state open

### team-habits
Run 1:1s and team operations with tangible artifacts.

**Parameters:**
- `label` (string): Issue label like 1-1 or action-item
- `title` (string): Issue title
- `body` (string): Issue body

**Commands:**
- `gh issue create --title '1:1 notes - 2026-08-10' --body 'Skip: roadmap; focus: growth areas' --repo owner/repo --label 1-1`
- `gh issue list --label 1-1 --state open --repo owner/repo`
- `gh api repos/{owner}/{repo}/issues/42/timeline -q '.[] | select(.event=="closed") | .actor.login'`
- `gh repo view owner/repo --json description,homepageUrl`
- `gh issue comment 42 --body 'Action item complete - evidence: PR #88'`

**Examples:**
- gh issue create --title '1:1 - ada' --body 'Follow-ups: onboarding checklist' --repo owner/repo
- gh issue list --label 1-1 --search 'state:open' --repo owner/repo
- gh issue comment 42 --body 'Resolution: agreed in retro'

## References
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Google re:Work Manager Guide](https://rework.withgoogle.com/en/guides/manager-guide/)
- [Engineering Manager Handbook](https://increment.com/teams/)
