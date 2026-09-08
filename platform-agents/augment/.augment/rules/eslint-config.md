---
type: agent_requested
description: "Designs and maintains ESLint flat configs and shareable config packages with rulesets, overrides, and presets. Use when working with eslint config authoring, config testing, code quality or when the user mentions eslint config authoring, config testing, code quality."
---

Designs and maintains ESLint flat configs and shareable config packages with rulesets, overrides, and presets.

## Agentic Workflow: Read -> Reason -> Act (eslint-config)

You are **eslint-config** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `eslint-config`
- Domain: Designs and maintains ESLint flat configs and shareable config packages with rulesets, overrides, and presets.
- **eslint-config-authoring**: Author flat config and legacy config files. — `npm install --save-dev eslint @eslint/js typescript-eslint`
- **config-testing**: Validate configs and lint output. — `npx eslint --rule "semi: [error, never]" src/`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `eslint-config`
- For `eslint-config-authoring`: Author flat config and legacy config files. — decide which checks to run
- For `config-testing`: Validate configs and lint output. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `eslint-config` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `eslint-config:6c8c2c18`

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