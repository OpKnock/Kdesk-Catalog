---
name: "lint-staged"
description: "Runs linters only on staged files via lint-staged git hooks, keeping pre-commit checks fast in any JS project. Use when working with lint staged hooks, code quality or when the user mentions lint staged hooks, code quality."
---

Runs linters only on staged files via lint-staged git hooks, keeping pre-commit checks fast in any JS project.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx lint-staged --allow-empty`
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

# Lint-Staged

Runs configured linters and formatters against only the files that are staged in git,
so pre-commit checks stay fast even in huge repos.

## When to Use

- Setting up a pre-commit hook that lints and auto-fixes changed files
- Speeding up a slow full-repo lint that blocks commits
- Enforcing formatting (Prettier) and linting (ESLint) only on touched files

## Real Commands

```bash
# Install with the husky pre-commit hook
npm install --save-dev lint-staged husky
npx husky init

# Add the hook
echo "npx lint-staged" > .husky/pre-commit

# Run on the current staging area (what the hook does)
npx lint-staged

# Run with output for debugging glob matching
npx lint-staged --debug

# Run linters one at a time
npx lint-staged --concurrent false

# Scope to a range of commits instead of the index
npx lint-staged --diff 'main...HEAD'
```

## Configuration (.lintstagedrc.json)

```json
{
  "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md,yml,yaml}": ["prettier --write"],
  "*.css": ["stylelint --fix", "prettier --write"],
  "*.py": ["black --check"]
}
```

## Testing

```bash
# Simulate what runs on commit
npx lint-staged --diff HEAD~1 --debug

# Verify the hook is installed
npx husky check
```

## Best Practices

- Combine `--fix`/`--write` linters so the file is fixed before commit
- Put slow checks (type-check, full test suite) in pre-push, not pre-commit
- Use explicit extensions, never `*` alone, to avoid binary files being formatted
- Keep the staged task list short; 3 steps max per glob

## Capabilities

### lint-staged-hooks
Configure and run lint-staged to execute linters and formatters on git-staged files

**Parameters:**
- `concurrent` (boolean): Run linter tasks in parallel (default true) or sequentially with false
- `diff` (string): Override the file list scope, e.g. 'main...HEAD'
- `allow-empty` (boolean): Allow empty commits when the staging area has no matching files

**Commands:**
- `npx lint-staged --allow-empty`
- `npx lint-staged --concurrent false`
- `npx lint-staged --debug`
- `npx lint-staged --diff 'main...HEAD'`
- `npx lint-staged --shell`

**Examples:**
- npx lint-staged
- npx lint-staged --concurrent false --debug
- git commit -m 'chore: format'  # triggers lint-staged via pre-commit hook

## References
- [lint-staged GitHub docs](https://github.com/okonet/lint-staged)
- [lint-staged configuration guide](https://github.com/okonet/lint-staged#configuration)
