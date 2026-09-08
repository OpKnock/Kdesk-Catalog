---
name: "documentation-generation"
description: "Auto-generates API reference documentation from source code and specs: Typedoc for TypeScript, sphinx-apidoc for Python, Doxygen for C++, and OpenAPI generators. Use when working with code doc gen, api or when the user mentions code doc gen, api."
license: "MIT"
compatibility: "Requires doxygen, jsdoc, npx, sphinx-apidoc."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(doxygen:*) Bash(jsdoc:*) Bash(npx:*) Bash(sphinx-apidoc:*)"
---

Auto-generates API reference documentation from source code and specs: Typedoc for TypeScript, sphinx-apidoc for Python, Doxygen for C++, and OpenAPI generators.

## Agentic Workflow: Read -> Reason -> Act (documentation-generation)

You are **Documentation Generation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `documentation-generation`
- Domain: Auto-generates API reference documentation from source code and specs: Typedoc for TypeScript, sphinx-apidoc for Python, Doxygen for C++, and OpenAPI generators.
- **code-doc-gen**: Generate API reference documentation from code and OpenAPI specs with the right tool per language. — `npx typedoc --out docs src/index.ts`
- Check `knowledge` and `prerequisites: doxygen, jsdoc, npx, sphinx-apidoc`

### 2. Reason — think for `documentation-generation`
- For `code-doc-gen`: Generate API reference documentation from code and OpenAPI specs with the right tool per language. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `documentation-generation` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Sphinx-apidoc` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `documentation-generation:c6318cd0`

# Documentation Generation

## What this skill does

Documentation generation extracts docs from source code: comments, docstrings, and types. This skill covers Typedoc (TS), sphinx-apidoc (Python), Doxygen (C++), jsdoc, and OpenAPI-based HTML generators.

## When to use

- Building an API reference that stays in sync with the code
- Onboarding a new team by generating module overviews
- Shipping docs as part of the release pipeline

## Real commands

```bash
# TypeScript
npx typedoc --out docs src/index.ts

# Python: build module docs, then render HTML
sphinx-apidoc -o docs/source src/api
sphinx-build -b html docs/source docs/build

# C/C++
doxygen Doxyfile

# OpenAPI -> static HTML reference
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g html2 -o docs
```

## Config example (jsdoc.json)

```json
{
  "source": {"include": ["src"]},
  "opts": {"destination": "docs", "recurse": true},
  "plugins": ["plugins/markdown"]
}
```

## CI integration

```bash
# Regenerate and fail on drift
npx typedoc --out docs src/index.ts && git diff --quiet docs/ || echo 'docs out of date'
```

## Best practices

- Generate on every merge; treat stale generated docs as a build failure.
- Keep doc comments on public API surfaces only.
- Use `--pretty` and sort options consistently so diffs stay small.
- Exclude generated/ and vendor/ from the source globs.

## Testing

```bash
# Verify all module pages rendered without warnings
sphinx-build -b html docs/source docs/build -W
```

## Capabilities

### code-doc-gen
Generate API reference documentation from code and OpenAPI specs with the right tool per language.

**Parameters:**
- `language` (string): Source language: typescript, python, cpp, javascript
- `source-dir` (string): Directory containing the source files to document
- `output-dir` (string): Directory for generated docs

**Commands:**
- `npx typedoc --out docs src/index.ts`
- `sphinx-apidoc -o docs/source src/api && sphinx-build -b html docs/source docs/build`
- `doxygen Doxyfile`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g html2 -o docs`
- `jsdoc -c jsdoc.json -d docs`

**Examples:**
- npx typedoc --out docs src/index.ts
- sphinx-apidoc -o docs/source src/api && sphinx-build -b html docs/source docs/build
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g html2 -o docs

## References
- [Typedoc Docs](https://typedoc.org/guides/overview/)
- [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
