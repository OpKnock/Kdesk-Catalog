---
trigger: glob
description: "Analyzes workforce DEI data with real tooling: org audit logs, survey analytics, representation metrics, and inclusive communication. Use when working with org data analytics, survey and text analysis or when the user mentions org data analytics, survey and text analysis."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Analyzes workforce DEI data with real tooling: org audit logs, survey analytics, representation metrics, and inclusive communication.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh api orgs/{org}/members --paginate | jq 'length'`, `jq 'group_by(.department) | map({dept: .[0].department, avg:`
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

# Diversity, Equity & Inclusion Analytics

Measure and improve workplace equity with reproducible data workflows.

## What This Skill Does

- Analyzes org/team composition via GitHub APIs
- Aggregates engagement survey scores by group
- Audits docs and code for exclusionary language
- Builds representation and retention metrics
- Produces trend reports for leadership

## When to Use

- Building a DEI measurement program
- Reviewing representation before hiring decisions
- Making communications more inclusive

## Real Commands

```bash
# Org data (GitHub)
gh api orgs/{org}/members --paginate | jq 'length'
gh api orgs/{org}/teams --paginate | jq '.[].name'
gh api repos/{owner}/{repo}/contributors --paginate   | jq '[.[].login] | unique | length'

# Survey analytics
jq 'group_by(.department) | map({dept: .[0].department, avg: ([.[].score] | add / length)})' survey.json
jq '[.responses[] | select(.score <= 2)] | length' survey.json

# Language audit
grep -rniE 'blacklist|whitelist|master/slave' --include='*.md' .
grep -rniE 'guys|manpower|sanity check' --include='*.md' .
```

## Metric Set

- Representation by team/level vs labor pool
- Engagement scores by demographic group
- Turnover and promotion rates by group
- Language inclusivity index over time

## Best Practices

- Aggregate small cells to protect privacy (min group size)
- Combine quantitative data with lived-experience feedback
- Publish trends, not raw individual data
- Re-run the same queries each quarter for comparability
- Pair analytics with concrete action plans

## Capabilities

### org-data-analytics
Pull and analyze org and team composition data from GitHub.

**Parameters:**
- `org` (string): GitHub org name
- `owner-repo` (string): owner/repo for contributor analysis

**Commands:**
- `gh api orgs/{org}/members --paginate | jq 'length'`
- `gh api orgs/{org}/teams --paginate | jq '.[].name'`
- `gh api rate_limit | jq '.resources.core'`
- `gh api repos/{owner}/{repo}/contributors --paginate | jq '[.[].login] | unique | length'`
- `gh api orgs/{org}/events --paginate | jq 'group_by(.type) | map({type: .[0].type, count: length})'`

**Examples:**
- gh api orgs/{org}/members --paginate | jq 'length'
- gh api repos/{owner}/{repo}/contributors --paginate | jq '[.[].login] | unique | length'
- gh api orgs/{org}/events --paginate | jq 'group_by(.type)'

### survey-and-text-analysis
Process engagement survey data and audit language in code/docs.

**Parameters:**
- `pattern` (string): Regex to audit for inclusive language
- `file` (string): Survey JSON file

**Commands:**
- `jq 'group_by(.department) | map({dept: .[0].department, avg: ([.[].score] | add / length)})' survey.json`
- `jq '[.responses[] | select(.score <= 2)] | length' survey.json`
- `grep -rniE 'guys|manpower|sanity check' --include='*.md' .`
- `grep -rniE 'blacklist|whitelist|master/slave' --include='*.md' .`
- `sort -u emails.txt | wc -l`

**Examples:**
- jq 'group_by(.department) | map({dept: .[0].department, avg: ([.[].score] | add / length)})' survey.json
- grep -rniE 'blacklist|whitelist' --include='*.md' .
- jq '[.responses[] | select(.score <= 2)] | length' survey.json

## References
- [GitHub REST API Orgs](https://docs.github.com/en/rest/orgs/orgs)
- [EEOC Employer Guidance](https://www.eeoc.gov/employers)
- [Inclusive Language Guide](https://developers.google.com/style/inclusive-documentation)
