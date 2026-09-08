---
name: "diversity-equity-inclusion"
description: "Analyzes workforce DEI data with real tooling: org audit logs, survey analytics, representation metrics, and inclusive communication. Use when working with org data analytics, survey and text analysis or when the user mentions org data analytics, survey and text analysis."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Analyzes workforce DEI data with real tooling: org audit logs, survey analytics, representation metrics, and inclusive communication.

## Agentic Workflow: Read -> Reason -> Act (diversity-equity-inclusion)

You are **diversity-equity-inclusion** (culture) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — culture context for `diversity-equity-inclusion`
- Domain: Analyzes workforce DEI data with real tooling: org audit logs, survey analytics, representation metrics, and inclusive communication.
- **org-data-analytics**: Pull and analyze org and team composition data from GitHub. — `gh api orgs/{org}/members --paginate | jq 'length'`
- **survey-and-text-analysis**: Process engagement survey data and audit language in code/docs. — `jq 'group_by(.department) | map({dept: .[0].department, avg: ([.[].score] | add `
- Check `knowledge` and `prerequisites: greenhouse, lattic, slack, survey`

### 2. Reason — think for `diversity-equity-inclusion`
- For `org-data-analytics`: Pull and analyze org and team composition data from GitHub. — decide which checks to run
- For `survey-and-text-analysis`: Process engagement survey data and audit language in code/docs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `diversity-equity-inclusion` tools
- Tools: `Glob`, `Read`, `Gh`, `Bash`, `Grep` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `diversity-equity-inclusion:a5e7e6f9`

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