---
name: "documentation-devtools"
description: "Builds project documentation sites with MkDocs, Sphinx, and Docusaurus: setup, build, serve, deploy, and API docs generation."
type: knowledge
triggers: ["documentation-devtools", "mkdocs", "sphinx-and-docusaurus"]
---

# documentation-devtools

Builds project documentation sites with MkDocs, Sphinx, and Docusaurus: setup, build, serve, deploy, and API docs generation.

## Instructions

# Documentation Engineering

Build and maintain documentation sites for projects.

## What This Skill Does

- Scaffolds MkDocs, Sphinx, and Docusaurus sites
- Builds static HTML from Markdown/reStructuredText
- Generates API references from code (Sphinx autodoc)
- Serves locally and deploys to GitHub Pages
- Enforces strict builds in CI

## When to Use

- A project needs a docs site, not just a README
- Automating API documentation generation
- Setting up docs CI with broken-link and strict checks

## Real Commands

```bash
# MkDocs
mkdocs new mydocs
cd mydocs && mkdocs serve
mkdocs build
mkdocs build --strict
mkdocs gh-deploy
mkdocs build --clean

# Sphinx
sphinx-quickstart docs
sphinx-build -b html docs docs/_build
make -C docs html
make -C docs doctest

# Docusaurus
npx create-docusaurus@latest site classic
npm run start --prefix site
npm run build --prefix site
npx docusaurus deploy
```

## mkdocs.yml Sketch

```yaml
site_name: My Project
nav:
  - Home: index.md
  - Guide: guide.md
theme: readthedocs
plugins:
  - search
```

## Best Practices

- Use --strict in CI so broken anchors fail builds
- Keep docs in-repo and version-tagged with releases
- Auto-generate API docs with autodoc/typedoc
- Add a docs contribution section to the main README
- Deploy from CI on main branch only

## Capabilities

### mkdocs
Create and build Python-based documentation sites from Markdown.

**Commands:**
- `mkdocs new mydocs`
- `mkdocs serve`
- `mkdocs build`
- `mkdocs gh-deploy`
- `mkdocs build --strict`
- `mkdocs build --clean`

**Examples:**
- mkdocs new mydocs
- mkdocs serve --dev-addr 127.0.0.1:8000
- mkdocs gh-deploy

### sphinx-and-docusaurus
Generate API docs with Sphinx and JS sites with Docusaurus.

**Commands:**
- `sphinx-quickstart docs`
- `sphinx-build -b html docs docs/_build`
- `make -C docs html`
- `npx create-docusaurus@latest site classic`
- `npm run build --prefix site`
- `npx docusaurus deploy`

**Examples:**
- sphinx-quickstart docs
- sphinx-build -b html docs docs/_build
- npm run build --prefix site
