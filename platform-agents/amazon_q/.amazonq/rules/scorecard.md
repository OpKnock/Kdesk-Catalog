Evaluates open-source project health and supply-chain risk with OSSF Scorecard, checking CI, code review, and dependency practices.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `scorecard --repo github.com/org/repo`, `scorecard --npm=lodash`
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