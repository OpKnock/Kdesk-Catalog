# leadership-development

Develops engineering leaders: PR review practice, contribution metrics, and team-level operational habits grounded in real GitHub workflows.

## Instructions

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