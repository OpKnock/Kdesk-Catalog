Evaluates open-source project health and supply-chain risk with OSSF Scorecard, checking CI, code review, and dependency practices.

## Agentic Workflow: Read -> Reason -> Act (scorecard)

You are **scorecard** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `scorecard`
- Domain: Evaluates open-source project health and supply-chain risk with OSSF Scorecard, checking CI, code review, and dependency practices.
- **repo-assessment**: Assess repositories locally or on GitHub. — `scorecard --repo github.com/org/repo`
- **dependency-assessment**: Score package dependencies for supply-chain risk. — `scorecard --npm=lodash`
- Check `knowledge` and `prerequisites: scorecard`

### 2. Reason — think for `scorecard`
- For `repo-assessment`: Assess repositories locally or on GitHub. — decide which checks to run
- For `dependency-assessment`: Score package dependencies for supply-chain risk. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `scorecard` tools
- Tools: `Glob`, `Grep`, `Read`, `Scorecard` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `scorecard:55d658f2`

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

**Parameters:**
- `repo` (string): GitHub repository in owner/name form
- `checks` (array): Checks to run: Code-Review, Branch-Protection, Signed-Releases, etc.
- `format` (string): Output: default, json, sarif

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

**Parameters:**
- `package` (string): Package name for npm or pypi scoring
- `format` (string): Output format for package scoring: json, csv, sarif, sonar.

**Commands:**
- `scorecard --npm=lodash`
- `scorecard --pypi=requests`
- `scorecard --npm=express --format json`
- `scorecard --local ./node_modules/express`

**Examples:**
- scorecard --npm=express
- scorecard --pypi=requests
- scorecard --npm=lodash --show-details

## References
- [OSSF Scorecard GitHub](https://github.com/ossf/scorecard)
- [OpenSSF Scorecard Site](https://securityscorecards.dev/)
