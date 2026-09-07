---
applyTo: "**/*.java **/*.r **/*.sh **/*.{js,ts,jsx,tsx} **/*.{ts,tsx}"
---

Designs and maintains ESLint flat configs and shareable config packages with rulesets, overrides, and presets.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install --save-dev eslint @eslint/js typescript-eslint`, `npx eslint --rule "semi: [error, never]" src/`
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

# ESLint Config

Design and maintain ESLint configuration.

## When to Use

- Setting up linting for new or existing JS/TS projects
- Building shareable config packages
- Migrating .eslintrc to flat config
- Tuning rules for a codebase

## Flat Config Example

```javascript
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist/**", "coverage/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      semi: ["error", "always"],
      "@typescript-eslint/no-explicit-any": "warn",
    },
  }
);
```

## Commands

```bash
npm install --save-dev eslint @eslint/js typescript-eslint

# Debug what config applies
npx eslint --print-config src/main.js
npx eslint --debug src/

# Environment info
npx eslint --env-info

# Rule experiments
npx eslint --rule "semi: [error, never]" src/
```

## Best Practices

- Start from recommended presets; add rules deliberately
- Use overrides for test files (globals, rules)
- Keep ignores in config, not scattered .eslintignore
- Test config changes with --print-config in CI
- Ship shareable configs as packages with semver
- Run npx eslint --debug to diagnose config merging

## Capabilities

### eslint-config-authoring
Author flat config and legacy config files.

**Parameters:**
- `config` (string): Config file path
- `target` (string): File to resolve config for

**Commands:**
- `npm install --save-dev eslint @eslint/js typescript-eslint`
- `npx eslint --init`
- `npx eslint --print-config src/main.js`
- `npx eslint --debug src/`
- `npx eslint --env-info`

**Examples:**
- npx eslint --print-config src/main.js | python -m json.tool | head -60
- npx eslint --config eslint.config.js src/
- npm install --save-dev eslint-plugin-react eslint-plugin-react-hooks

### config-testing
Validate configs and lint output.

**Parameters:**
- `rule` (string): Inline rule override
- `ext` (string): File extensions to lint

**Commands:**
- `npx eslint --rule "semi: [error, never]" src/`
- `npx eslint --rulesdir ./custom-rules src/`
- `npx eslint --no-eslintrc --env browser src/`
- `npx eslint --ext .js,.ts src/`

**Examples:**
- npx eslint --rule "quotes: [error, single]" src/
- npx eslint --no-eslintrc --config base.js src/

## References
- [ESLint Config Guide](https://eslint.org/docs/latest/use/configure/)
- [typescript-eslint Docs](https://typescript-eslint.io)
