---
name: "scorecard"
description: "Evaluates open-source project health and supply-chain risk with OSSF Scorecard, checking CI, code review, and dependency practices."
type: knowledge
triggers: ["scorecard", "repo-assessment", "dependency-assessment"]
---

# scorecard

Evaluates open-source project health and supply-chain risk with OSSF Scorecard, checking CI, code review, and dependency practices.

## Instructions

# OSSF Scorecard

Automated supply-chain risk scoring for open-source projects and dependencies.

## What This Skill Does

- Scores repos on branch protection, code review, CI, and signing
- Assesses npm/pypi packages before adoption
- Reports per-check evidence and remediation guidance
- Integrates into dependency-review workflows via SARIF

## When to Use

- Vetting a third-party dependency for production use
- Auditing your own repo's security posture
- Supply-chain due diligence reports

## Real Commands

```bash
# Assess a repository
scorecard --repo github.com/org/repo
scorecard --repo github.com/org/repo --show-details

# Local directory
scorecard --local .

# Targeted checks
scorecard --repo github.com/org/repo --checks Code-Review,Branch-Protection

# Packages
scorecard --npm=express
scorecard --pypi=requests

# Machine-readable
scorecard --repo github.com/org/repo --format json
```

## Reading Scores

- 0-4: critical gaps (no CI, no review, no signing)
- 5-7: partial hygiene (some automation, gaps in release processes)
- 8-10: strong practices (protected branches, signed releases, fuzzing)

## Best Practices

- Gate dependency adoption on a minimum score (e.g. >= 6)
- Re-run scorecard quarterly on critical dependencies
- Fix the highest-weight checks first: Branch-Protection and Code-Review
- Combine with Dependabot alerts and SBOMs for the full picture
- Run scorecard on your own repos in CI and track the trend

## Capabilities

### repo-assessment
Assess repositories locally or on GitHub.

**Commands:**
- `scorecard --repo github.com/org/repo`
- `scorecard --local .`
- `scorecard --repo github.com/org/repo --checks Code-Review,Branch-Protection`
- `scorecard --repo github.com/org/repo --show-details`
- `scorecard --repo github.com/org/repo --format json`

**Examples:**
- scorecard --repo github.com/kubernetes/kubernetes
- scorecard --local .
- scorecard --repo github.com/org/repo --show-details

### dependency-assessment
Score package dependencies for supply-chain risk.

**Commands:**
- `scorecard --npm=lodash`
- `scorecard --pypi=requests`
- `scorecard --npm=express --format json`
- `scorecard --local ./node_modules/express`

**Examples:**
- scorecard --npm=express
- scorecard --pypi=requests
- scorecard --npm=lodash --show-details
