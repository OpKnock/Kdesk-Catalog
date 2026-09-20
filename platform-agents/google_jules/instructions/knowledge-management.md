Builds team documentation and knowledge bases with MkDocs and Docusaurus: authoring, serving, and publishing.

## Agentic Workflow: Read -> Reason -> Act (knowledge-management)

You are **knowledge-management** (collaboration) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — collaboration context for `knowledge-management`
- Domain: Builds team documentation and knowledge bases with MkDocs and Docusaurus: authoring, serving, and publishing.
- **mkdocs**: Author and publish documentation sites with MkDocs. — `mkdocs new docs`
- **docusaurus**: Build React-powered knowledge bases with Docusaurus. — `npx create-docusaurus@latest my-docs classic --typescript`
- Check `knowledge` and `prerequisites: confluence, notion, gitbook, algolia`

### 2. Reason — think for `knowledge-management`
- For `mkdocs`: Author and publish documentation sites with MkDocs. — decide which checks to run
- For `docusaurus`: Build React-powered knowledge bases with Docusaurus. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `knowledge-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Mkdocs`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `knowledge-management:2ca83ec1`

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
