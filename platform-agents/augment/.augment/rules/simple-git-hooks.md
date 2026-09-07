---
type: agent_requested
description: "Configures git hooks via package.json with simple-git-hooks, a zero-dependency alternative to husky. Use when working with simple git hooks, code quality or when the user mentions simple git hooks, code quality."
---

Configures git hooks via package.json with simple-git-hooks, a zero-dependency alternative to husky.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx simple-git-hooks`
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

# Simple Git Hooks

Declares git hooks directly in package.json without husky's shell wrapper or
additional dependencies.

## When to Use

- Lightweight pre-commit/pre-push hooks for JS projects
- Teams that want hook config visible in package.json
- Replacing husky in projects that avoid extra deps

## Real Commands

```bash
# Install the tool
npm install --save-dev simple-git-hooks

# Configure hooks in package.json
npm pkg set simple-git-hooks.pre-commit="npx lint-staged"
npm pkg set simple-git-hooks.pre-push="npm test"

# Install the hooks into .git/hooks
npx simple-git-hooks

# Verify installed hooks match config
npx simple-git-hooks --validate

# Remove all managed hooks
npx simple-git-hooks --remove
```

## Config in package.json

```json
{
  "simple-git-hooks": {
    "pre-commit": "npx lint-staged",
    "pre-push": "npm test",
    "commit-msg": "npx commitlint --edit $1"
  }
}
```

## postinstall for teammates

```json
{
  "scripts": {
    "postinstall": "node -e \"try{require('simple-git-hooks')()}catch(e){}\""
  }
}
```

## Best Practices

- Always run `npx simple-git-hooks --validate` after changing config
- Add the postinstall script so `npm install` refreshes hooks
- Keep hook commands fast; move heavy checks to pre-push or CI
- Note that hooks are per-clone (in .git/hooks) - reinstall after fresh clone

## Example Response

Confirms which hooks were installed (pre-commit, pre-push), validates them against
package.json, and shows the command each hook will run.

## Capabilities

### simple-git-hooks
Install, validate, and update git hooks declared in package.json

**Parameters:**
- `config` (string): Path to an alternative config file
- `validate` (boolean): Check that installed hooks match the config
- `remove` (boolean): Remove all git hooks managed by simple-git-hooks

**Commands:**
- `npx simple-git-hooks`
- `npx simple-git-hooks --validate`
- `npx simple-git-hooks --remove`
- `npm pkg set simple-git-hooks.pre-commit="npx lint-staged"`
- `npx simple-git-hooks --config .simple-git-hooks.json`

**Examples:**
- npm pkg set simple-git-hooks.pre-push="npm test"
- npx simple-git-hooks --validate
- node -e "require('simple-git-hooks')()"

## References
- [simple-git-hooks GitHub](https://github.com/toplenboren/simple-git-hooks)
- [Git hooks reference](https://git-scm.com/docs/githooks)