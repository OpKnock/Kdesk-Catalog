---
name: "husky"
description: "Configures Git hooks with husky: pre-commit, commit-msg, pre-push gates, and lint-staged integration. Use when working with husky setup, husky lint staged, code quality or when the user mentions husky setup, husky lint staged, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Configures Git hooks with husky: pre-commit, commit-msg, pre-push gates, and lint-staged integration.

## Agentic Workflow: Read -> Reason -> Act (husky)

You are **husky** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `husky`
- Domain: Configures Git hooks with husky: pre-commit, commit-msg, pre-push gates, and lint-staged integration.
- **husky-setup**: Initialize and manage husky hooks. — `npx husky init`
- **husky-lint-staged**: Run staged-file checks with lint-staged. — `npm install --save-dev lint-staged`
- Check `knowledge` and `prerequisites: git, npm, npx`

### 2. Reason — think for `husky`
- For `husky-setup`: Initialize and manage husky hooks. — decide which checks to run
- For `husky-lint-staged`: Run staged-file checks with lint-staged. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `husky` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `husky:460e628a`

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