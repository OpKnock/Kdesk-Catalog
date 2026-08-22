# husky

Configures Git hooks with husky: pre-commit, commit-msg, pre-push gates, and lint-staged integration.

## Instructions

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

**Commands:**
- `npm install --save-dev lint-staged`
- `npx lint-staged`
- `npx lint-staged --diff "src/**/*.ts"`
- `npx lint-staged --allow-empty`

**Examples:**
- npx lint-staged --concurrent 4
- npx lint-staged --no-stash
