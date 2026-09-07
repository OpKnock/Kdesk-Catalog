---
type: agent_requested
description: "Designs API governance programs: style guide structure, ruleset architecture, and enforcement workflows before rollout. Use when working with governance design, workflow design or when the user mentions governance design, workflow design."
---

Designs API governance programs: style guide structure, ruleset architecture, and enforcement workflows before rollout.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mkdir -p rules/guides rules/functions tests/fixtures`, `node -e "console.log('flow: lint -> diff -> review -> approv`
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

# API Gov (Design)

Designs the governance program before enforcing it: rules, tiers, and workflows.

## When to Use
- Planning governance for many teams
- Avoiding over-strict rule sets
- Documenting review and waiver flows

## Real Commands

```bash
# Layout
mkdir -p rules/guides rules/functions tests/fixtures

# Draft rule docs
node -e "const fs=require('fs');fs.writeFileSync('rules/guides/naming.yaml','# naming rules\n')"

# Fixtures for testing rules
python -c "open('tests/fixtures/bad.yaml','w').write('paths:\n  /BadPath:\n')"

# Exception process
node -e "const fs=require('fs');fs.writeFileSync('docs/EXCEPTIONS.md','# Exceptions\n\n1. Submit waiver PR\n2. Time-box 30 days\n')"
```

## Design Decisions
- Three tiers: recommended, org, strict
- One rule doc per domain
- Fixtures per rule for automated tests

## Workflow Design
lint -> diff -> human review -> approve; waivers are PRs with expiry.

## Testing
Validate every new rule against fixtures before rollout.

## Best Practices
- Enforce incrementally: warn first, error later

## Capabilities

### governance-design
Structure style guides and rulesets with severity tiers and scopes

**Parameters:**
- `tier` (string): Rule severity tier
- `domain` (string): Rule domain: naming, errors, pagination

**Commands:**
- `mkdir -p rules/guides rules/functions tests/fixtures`
- `node -e "const fs=require('fs');fs.writeFileSync('rules/guides/naming.yaml','# naming rules\n')"`
- `node -e "const fs=require('fs');fs.writeFileSync('rules/guides/errors.yaml','# error rules\n')"`
- `node -e "console.log('tiers: recommended > org > strict')"`
- `python -c "open('tests/fixtures/bad.yaml','w').write('paths:\n  /BadPath:\n')"`

**Examples:**
- mkdir -p rules/guides rules/functions tests/fixtures
- node -e "const fs=require('fs');fs.writeFileSync('rules/guides/naming.yaml','# naming rules\n')"
- python -c "open('tests/fixtures/bad.yaml','w').write('paths:\n  /BadPath:\n')"

### workflow-design
Design review workflows: who reviews, what CI checks, exception process

**Parameters:**
- `waiverDays` (string): Waiver duration
- `gate` (string): CI gate severity

**Commands:**
- `node -e "console.log('flow: lint -> diff -> review -> approve')"`
- `python -c "print('gate: fail on error severity')"`
- `node -e "const fs=require('fs');fs.writeFileSync('docs/EXCEPTIONS.md','# Exceptions\n\n1. Submit waiver PR\n2. Time-box 30 days\n')"`
- `python -c "print('review cadence: weekly')"`
- `git add docs/EXCEPTIONS.md && git commit -m 'document exception process'`

**Examples:**
- node -e "const fs=require('fs');fs.writeFileSync('docs/EXCEPTIONS.md','# Exceptions\n\n1. Submit waiver PR\n2. Time-box 30 days\n')"
- node -e "console.log('flow: lint -> diff -> review -> approve')"
- git add docs/EXCEPTIONS.md && git commit -m 'document exception process'

## References
- [Spectral Ruleset Design](https://docs.stoplight.io/docs/spectral/reference/rulesets)
- [Governance Maturity](https://www.getambassador.io/resources/api-governance)