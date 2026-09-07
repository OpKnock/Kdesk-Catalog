Implements API governance from scratch: baseline Spectral rulesets, style guide docs, and first CI lint gate.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g @stoplight/spectral-cli`, `mkdir -p docs/api-guide`
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

# API Gov (Bootstrap)

Stands up governance for a team or org that has none: baseline linting, a style guide, and a first CI gate.

## When to Use
- No API standards exist yet
- Teams ship inconsistent APIs
- Starting governance incrementally

## Real Commands

```bash
# Install
npm install -g @stoplight/spectral-cli
npx @stoplight/spectral-cli lint --version

# Baseline lint
npx @stoplight/spectral-cli lint --extends spectral:oas openapi.yaml

# With project ruleset
npx @stoplight/spectral-cli lint --extends spectral:oas --ruleset .spectral.yaml openapi.yaml
```

## Style Guide

```bash
mkdir -p docs/api-guide
python -c "open('docs/api-guide/STYLE.md','w').write('# API Style Guide\n\n- Plural nouns for collections\n- RFC 9457 errors\n- Pagination via page/limit\n')"
```

## First CI Gate
Run the baseline lint in CI with `--fail-severity error`.

## Testing
Fix or annotate existing violations before enabling the gate org-wide.

## Best Practices
- Start with recommended rules; add custom ones later
- Publish the guide where developers already read docs

## Capabilities

### governance-bootstrap
Stand up initial linting with recommended rules and a project ruleset

**Parameters:**
- `extends` (string): Base ruleset to extend
- `spec` (string): Spec path

**Commands:**
- `npm install -g @stoplight/spectral-cli`
- `npx @stoplight/spectral-cli lint --extends spectral:oas openapi.yaml`
- `npx @stoplight/spectral-cli lint --extends spectral:oas --ruleset .spectral.yaml openapi.yaml`
- `npx @stoplight/spectral-cli lint --version`
- `npx @stoplight/spectral-cli lint --help`

**Examples:**
- npx @stoplight/spectral-cli lint --extends spectral:oas openapi.yaml
- npx @stoplight/spectral-cli lint --extends spectral:oas --ruleset .spectral.yaml openapi.yaml
- npm install -g @stoplight/spectral-cli && npx @stoplight/spectral-cli lint --version

### style-guide-authoring
Write and publish the API style guide that rules enforce

**Parameters:**
- `guideDir` (string): Docs directory for the style guide
- `rules` (string): Rules to document

**Commands:**
- `mkdir -p docs/api-guide`
- `node -e "const fs=require('fs');fs.writeFileSync('docs/api-guide/STYLE.md','# API Style Guide\n\n- Resources are plural nouns\n- Errors use RFC 9457\n')"`
- `node -e "console.log('naming: kebab-case paths') "`
- `python -c "open('docs/api-guide/ERRORS.md','w').write('# Error Codes\n')"`
- `git add docs/api-guide && git commit -m 'publish API style guide'`

**Examples:**
- node -e "const fs=require('fs');fs.writeFileSync('docs/api-guide/STYLE.md','# API Style Guide\n\n- Resources are plural nouns\n- Errors use RFC 9457\n')"
- python -c "open('docs/api-guide/ERRORS.md','w').write('# Error Codes\n')"
- git add docs/api-guide && git commit -m 'publish API style guide'

## References
- [Spectral CLI](https://docs.stoplight.io/docs/spectral/reference/cli)
- [OpenAPI Guidelines](https://opensource.zalando.com/restful-api-guidelines/)