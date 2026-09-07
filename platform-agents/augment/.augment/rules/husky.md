---
type: agent_requested
description: "Configures Git hooks with husky: pre-commit, commit-msg, pre-push gates, and lint-staged integration. Use when working with husky setup, husky lint staged, code quality or when the user mentions husky setup, husky lint staged, code quality."
---

Configures Git hooks with husky: pre-commit, commit-msg, pre-push gates, and lint-staged integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx husky init`, `npm install --save-dev lint-staged`
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

# Husky

Git hooks made easy.

## When to Use

- Running tests and lint before commits
- Validating commit messages with commitlint
- Pre-push builds and checks
- Keeping CI from being the first line of defense

## Commands

```bash
# Init
npx husky init

# Add hooks
npx husky add .husky/pre-commit "npm test"
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/commit-msg "npx commitlint --edit \"$1\""
npx husky add .husky/pre-push "npm run build"

# Verify hooks path
git config core.hooksPath
```

## lint-staged Config

```json
// package.json
{
  "lint-staged": {
    "*.{js,ts}": ["eslint --fix", "prettier --write"],
    "*.py": ["black", "flake8"]
  }
}
```

## Best Practices

- Run fast checks in pre-commit (lint + format)
- Use lint-staged so only changed files are checked
- Keep commit-msg validation strict with commitlint
- Make pre-push run tests and builds
- In CI, skip hooks: set HUSKY=0 for checkout steps
- Commit .husky/ so all developers share the hooks

## Capabilities

### husky-setup
Initialize and manage husky hooks.

**Parameters:**
- `hook` (string): Hook name: pre-commit, commit-msg, pre-push
- `command` (string): Command to run

**Commands:**
- `npx husky init`
- `npx husky add .husky/pre-commit "npm test"`
- `npx husky add .husky/commit-msg "npx commitlint --edit \\"$1\\""`
- `git config core.hooksPath`
- `npx husky set .husky/pre-push "npm run build"`

**Examples:**
- npx husky add .husky/pre-commit "npx lint-staged"
- npx husky add .husky/pre-push "npm test"
- git config core.hooksPath .husky

### husky-lint-staged
Run staged-file checks with lint-staged.

**Parameters:**
- `glob` (string): File pattern
- `config` (string): lint-staged config path

**Commands:**
- `npm install --save-dev lint-staged`
- `npx lint-staged`
- `npx lint-staged --diff "src/**/*.ts"`
- `npx lint-staged --allow-empty`

**Examples:**
- npx lint-staged --concurrent 4
- npx lint-staged --no-stash

## References
- [Husky Docs](https://typicode.github.io/husky/)
- [lint-staged Docs](https://github.com/lint-staged/lint-staged)