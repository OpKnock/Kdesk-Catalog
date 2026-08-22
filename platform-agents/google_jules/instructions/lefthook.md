# lefthook

Manages Git hooks with Lefthook: parallel fast hooks, commands per glob, and CI-friendly behavior.

## Instructions

# Lefthook

Fast, parallel Git hooks.

## When to Use

- Running many lint checks quickly before commits
- Language-agnostic hook config (JS, Python, Go, Ruby)
- CI-friendly hooks with force mode
- Replacing husky/pre-commit setups

## Commands

```bash
# Setup
lefthook install
lefthook add pre-commit
lefthook uninstall

# Run manually
lefthook run pre-commit
lefthook run pre-commit --all-files
lefthook run commit-msg --file .git/COMMIT_EDITMSG

# Debug
lefthook run --debug pre-commit
lefthook run --dry-run pre-commit
```

## Config Example

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    eslint:
      glob: "*.{js,ts}"
      run: npx eslint {staged_files} --fix
    prettier:
      glob: "*.{js,ts,json,md}"
      run: npx prettier --write {staged_files}
    pytest:
      glob: "*.py"
      run: pytest -q {staged_files}
```

## Best Practices

- Use parallel: true with independent commands
- Scope commands with glob so checks run on the right files
- Use {staged_files} and {all_files} variables precisely
- Add a pre-push hook for slow full test runs
- Use lefthook run --debug to fix hook issues
- Commit lefthook.yml so all devs share the config

## Capabilities

### lefthook-setup
Install and configure Lefthook.

**Commands:**
- `lefthook install`
- `lefthook add pre-commit`
- `lefthook uninstall`
- `lefthook version`
- `lefthook install -f`

**Examples:**
- lefthook install -f
- lefthook add commit-msg
- lefthook run pre-commit

### lefthook-run
Run hooks manually and debug.

**Commands:**
- `lefthook run pre-commit`
- `lefthook run pre-commit --all-files`
- `lefthook run commit-msg --file .git/COMMIT_EDITMSG`
- `lefthook run --debug pre-commit`
- `lefthook run pre-push --force`

**Examples:**
- lefthook run pre-commit --skip-output
- lefthook run lint --only-files
- lefthook run --dry-run pre-commit
