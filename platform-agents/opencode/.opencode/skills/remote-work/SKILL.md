---
name: "remote-work"
description: "Runs distributed-team operations: async documentation, calendar visibility, and GitHub-first collaboration rituals. Use when working with async docs, calendar or when the user mentions async docs, calendar."
---

Runs distributed-team operations: async documentation, calendar visibility, and GitHub-first collaboration rituals.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `markdownlint README.md`, `gcalcli agenda 'tomorrow'`
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

# Remote Work

Make distributed work visible, documented, and humane.

## When to Use

- Teams across timezones
- Asynchronous decision making
- Calendar transparency and focus time

## Async-first rules

- Write decisions down: RFCs and decision logs beat meetings.
- Default to pull requests and issues over chat.
- Reply within the agreed SLA (24h), not instantly.

## Documentation hygiene

```bash
markdownlint README.md
npx prettier --check 'docs/**/*.md'
```

## Calendar transparency

```bash
gcalcli agenda 'tomorrow'
gcalcli calw 3
gcalcli quickadd 'Deep work 09:00-11:00'
```

Block focus time visibly; the calendar is the team's availability signal.

## Meeting rhythm

- 1:1s async-first: agenda docs before the call.
- Record decisions in issues, not meeting minutes.
- Timezone rotation for global standups.

## Best practices

- Keep a public 'what I'm working on' thread per week.
- Update docs before asking questions in chat.
- Respect focus blocks; batch interruptions.
- Ergonomic setup: quality headset, lighting, stable network.

## Testing

Audit that every active decision has a doc link and every issue has a comment trail.

## Capabilities

### async-docs
Maintain the async-first documentation practice.

**Parameters:**
- `pattern` (string): File glob for linting
- `config` (string): markdownlint config
- `check` (string): Check-only mode for prettier

**Commands:**
- `markdownlint README.md`
- `npx prettier --check 'docs/**/*.md'`
- `git diff --check`
- `gh pr create --title 'RFC: cache strategy' --body 'RFC body with decision log'`
- `gh issue comment 42 --body 'Async update: milestone adjusted - see link'`

**Examples:**
- npx prettier --write 'docs/**/*.md'
- markdownlint docs/ --config .markdownlint.json
- gh pr create --draft --title 'WIP: onboarding guide'

### calendar
Keep visibility across timezones with gcalcli.

**Parameters:**
- `query` (string): Event search term
- `days` (number): Week view days
- `cal` (string): Calendar name

**Commands:**
- `gcalcli agenda 'tomorrow'`
- `gcalcli calw 3`
- `gcalcli quickadd 'Deep work 09:00-11:00'`
- `gcalcli search 'standup' --ts`
- `gcalcli calquery --cal 'Team Sync' --ts`

**Examples:**
- gcalcli agenda today --nostarted
- gcalcli quickadd '1:1 with Ada tomorrow 15:00' --cal 'Meetings'
- gcalcli calw 1 --military

## References
- [GitLab Communication Handbook](https://handbook.gitlab.com/handbook/communication/)
- [gcalcli](https://github.com/insanum/gcalcli)
- [markdownlint](https://github.com/DavidAnson/markdownlint)
