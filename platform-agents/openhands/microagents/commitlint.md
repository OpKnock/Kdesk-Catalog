---
name: "commitlint"
description: "Enforces conventional commit message standards with commitlint: configs, hooks, and CI validation. Use when working with commitlint cli, commitlint config, code quality or when the user mentions commitlint cli, commitlint config, code quality."
type: knowledge
triggers: ["commitlint", "commitlint-cli", "commitlint-config"]
---

Enforces conventional commit message standards with commitlint: configs, hooks, and CI validation.

## Agentic Workflow: Read -> Reason -> Act (commitlint)

You are **commitlint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `commitlint`
- Domain: Enforces conventional commit message standards with commitlint: configs, hooks, and CI validation.
- **commitlint-cli**: Lint commit messages from stdin or files. — `npx commitlint --from HEAD~1 --to HEAD`
- **commitlint-config**: Configure rules and plugins. — `npm install --save-dev @commitlint/cli @commitlint/config-conventional`
- Check `knowledge` and `prerequisites: echo, npm, npx`

### 2. Reason — think for `commitlint`
- For `commitlint-cli`: Lint commit messages from stdin or files. — decide which checks to run
- For `commitlint-config`: Configure rules and plugins. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `commitlint` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Echo` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `commitlint:2c9a2269`

# commitlint

Validate commit message conventions.

## When to Use

- Enforcing Conventional Commits in a repo
- Generating changelogs from message structure
- Keeping git history greppable and machine-readable
- Standardizing scope and type usage across teams

## Format

```
type(scope): subject

body

footer
```

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

## Commands

```bash
# Install
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Lint a commit range
npx commitlint --from HEAD~1 --to HEAD

# Lint stdin
echo "feat: add login" | npx commitlint
echo "add stuff" | npx commitlint   # fails

# Edit hook (pre-commit in hooks scripts)
npx commitlint --edit "$1"

# Inspect config
npx commitlint --print-config
```

## Config Example

```javascript
// commitlint.config.cjs
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "subject-case": [2, "never", ["sentence-case", "start-case"]],
    "type-enum": [2, "always", ["feat", "fix", "docs", "chore", "test"]],
  },
};
```

## Best Practices

- Run commitlint --edit in the commit-msg hook
- Use the conventional preset unless rules are justified
- Keep subjects under 100 chars and imperative tense
- Add scope for the affected module: fix(api):
- Run --from HEAD~1 in CI for all pushed commits

## Capabilities

### commitlint-cli
Lint commit messages from stdin or files.

**Parameters:**
- `from` (string): Lower commit boundary
- `to` (string): Upper commit boundary

**Commands:**
- `npx commitlint --from HEAD~1 --to HEAD`
- `npx commitlint --from HEAD~10`
- `echo "feat: add login" | npx commitlint`
- `echo "add stuff" | npx commitlint`

**Examples:**
- npx commitlint --from HEAD~1 --to HEAD --verbose
- npx commitlint --edit "$1"
- echo "fix(api): handle timeout" | npx commitlint --verbose

### commitlint-config
Configure rules and plugins.

**Parameters:**
- `config` (string): Config file path
- `rule` (string): Rule name to override

**Commands:**
- `npm install --save-dev @commitlint/cli @commitlint/config-conventional`
- `npx commitlint --init`
- `npx commitlint --print-config`
- `npm install --save-dev @commitlint/cz-commitlint`

**Examples:**
- npx commitlint --print-config | head -40
- echo "module.exports = {extends: [\"@commitlint/config-conventional\"]}" > commitlint.config.cjs

## References
- [commitlint Docs](https://commitlint.js.org)
- [Conventional Commits](https://www.conventionalcommits.org)
