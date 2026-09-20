---
applyTo: "**/*.r **/*.sh"
---

Creates and maintains operational runbooks with MkDocs and mdBook, including alerts-to-runbook linking and searchable playbooks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mkdocs new runbooks`, `mkdocs build --clean`
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

# Runbooks

Operational playbooks that turn alerts into confident actions.

## What This Skill Does

- Scaffolds a searchable runbook site with MkDocs
- Structures playbooks: symptoms, diagnosis, fix, verify
- Links alerts to runbooks for one-click context
- Keeps runbooks fresh with linting and TODOs

## When to Use

- An alert needs a documented response path
- Onboarding new on-call engineers
- Centralizing operational knowledge

## Real Commands

```bash
# Scaffold and preview
mkdocs new runbooks
cd runbooks && mkdocs serve
mkdocs build --strict
mkdocs gh-deploy

# Maintain
mkdocs build --clean
npx markdownlint-cli runbooks/**/*.md
grep -rl 'TODO' runbooks/
```

## Runbook Template

```markdown
# High API Error Rate

## Symptoms
- 5xx rate > 1% for 5 minutes
- SLO burn rate > 1

## Diagnosis
1. Check k8s events: kubectl get events --sort-by=.lastTimestamp
2. Check deploys in the last hour

## Fix
1. Roll back: kubectl rollout undo deployment/api
2. Scale out if resource-bound

## Verify
- 5xx rate below 0.1% for 10 minutes
- Alert resolves
```

## Best Practices

- One runbook per alert; keep the alert label pointing to it
- Write for the tired on-call engineer at 3am
- Version-control runbooks with the service code
- Review runbooks after every incident (update, don't rearchive)
- Test runbooks in game days; mark last-tested dates

## Capabilities

### runbook-authoring
Scaffold, write, and preview runbook documentation sites.

**Parameters:**
- `project` (string): Docs project directory name
- `strict` (boolean): Fail build on warnings

**Commands:**
- `mkdocs new runbooks`
- `mkdocs serve`
- `mkdocs build`
- `mkdocs gh-deploy`
- `mkdocs build --strict`

**Examples:**
- mkdocs new runbooks && cd runbooks && mkdocs serve
- mkdocs build --strict
- mkdocs gh-deploy

### runbook-maintenance
Maintain search index, structure, and quality.

**Parameters:**
- `dir` (string): Docs directory to lint or search
- `port` (integer): Port for the local mkdocs preview server.

**Commands:**
- `mkdocs build --clean`
- `grep -rl '`
- `npx markdownlint-cli runbooks/**/*.md`
- `mkdocs serve -a 0.0.0.0:8000`
- `mdbook build`

**Examples:**
- npx markdownlint-cli runbooks/**/*.md
- mkdocs build --clean
- grep -rl '

## References
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Google SRE Runbook Guidance](https://sre.google/workbook/incident-response/)
- [mdBook Documentation](https://rust-lang.github.io/mdBook/)
