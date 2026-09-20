---
name: "api-gov-governance-design"
description: "Designs API governance programs: style guide structure, ruleset architecture, and enforcement workflows before rollout."
type: knowledge
triggers: ["api-gov-governance-design", "governance-design", "workflow-design"]
---

# Api Gov Governance Design

Designs API governance programs: style guide structure, ruleset architecture, and enforcement workflows before rollout.

## Instructions

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
