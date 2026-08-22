# lint-staged

Runs linters only on staged files via lint-staged git hooks, keeping pre-commit checks fast in any JS project.

## Instructions

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