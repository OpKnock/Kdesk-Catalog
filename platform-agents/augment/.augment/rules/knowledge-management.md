---
type: agent_requested
description: "Builds team documentation and knowledge bases with MkDocs and Docusaurus: authoring, serving, and publishing. Use when working with mkdocs, docusaurus or when the user mentions mkdocs, docusaurus."
---

Builds team documentation and knowledge bases with MkDocs and Docusaurus: authoring, serving, and publishing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mkdocs new docs`, `npx create-docusaurus@latest my-docs classic --typescript`
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

# Knowledge Management

Turn team knowledge into a maintainable documentation site.

## When to Use

- Onboarding and runbook documentation
- API and product docs that need versioning
- Centralizing tribal knowledge from Slack/meetings

## MkDocs for lightweight docs

```yaml
site_name: Platform Docs
nav:
  - Home: index.md
  - Runbooks: runbooks.md
  - Architecture: architecture.md
theme: material
```

```bash
mkdocs new docs
mkdocs serve -a localhost:8000
mkdocs build --strict
```

`--strict` turns warnings into errors - great CI gate.

## Publish to GitHub Pages

```bash
mkdocs gh-deploy
```

## Docusaurus for feature-rich docs

```bash
npx create-docusaurus@latest my-docs classic --typescript
npm run start
npm run build
```

## Documentation hygiene

- Every runbook starts with impact + owner + recovery steps.
- Link docs from code comments and alert pages.
- Mark stale docs with expiry dates; delete rather than rot.
- Keep a docs review task in the team's sprint.

## Best practices

- Single source of truth: link, don't duplicate.
- Use mermaid diagrams for architecture flows.
- Version docs with product versions.
- CI: build --strict on every PR touching docs/

## Testing

```bash
mkdocs build --strict
```

Verify all internal links resolve before merge.

## Capabilities

### mkdocs
Author and publish documentation sites with MkDocs.

**Parameters:**
- `strict` (string): Fail on warnings
- `site-dir` (string): Output directory for the site
- `serve` (string): Dev server with host:port

**Commands:**
- `mkdocs new docs`
- `mkdocs serve -a localhost:8000`
- `mkdocs build --strict`
- `mkdocs gh-deploy`
- `mkdocs build --clean`

**Examples:**
- mkdocs serve -a 0.0.0.0:8000 --livereload
- mkdocs build --strict --site-dir dist
- mkdocs gh-deploy --force

### docusaurus
Build React-powered knowledge bases with Docusaurus.

**Parameters:**
- `template` (string): classic or plain template
- `port` (number): Dev server port
- `locale` (string): Translation locale

**Commands:**
- `npx create-docusaurus@latest my-docs classic --typescript`
- `npm run start`
- `npm run build`
- `npm run swizzle @docusaurus/theme-classic SidebarItem -- --typescript`
- `npx docusaurus serve`

**Examples:**
- npx create-docusaurus@latest my-docs classic --typescript --skip-install
- npm run build && npx docusaurus serve --port 3001
- npm run write-translations -- --locale de

## References
- [MkDocs](https://www.mkdocs.org/)
- [Docusaurus](https://docusaurus.io/docs)
- [Markdown Guide](https://www.markdownguide.org/)