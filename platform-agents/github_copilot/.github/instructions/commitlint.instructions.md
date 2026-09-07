---
applyTo: "**/*.java **/*.r **/*.sh **/*.{js,ts,jsx,tsx}"
---

Enforces conventional commit message standards with commitlint: configs, hooks, and CI validation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx commitlint --from HEAD~1 --to HEAD`, `npm install --save-dev @commitlint/cli @commitlint/config-co`
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
